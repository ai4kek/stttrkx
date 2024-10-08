#!/usr/bin/env python
# coding: utf-8

"""Mininally modified version of 'Step_5_Build_Track_Candidates.py' script from
exatrkx-hsf/Examples/TrackML_Quickstart/Scripts repository to build tracks."""

import sys
import os
import yaml
import argparse
import logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s:%(message)s')
import torch
import numpy as np
import scipy.sparse as sps

from tqdm.contrib.concurrent import process_map
from tqdm import tqdm
from functools import partial

device = 'cuda' if torch.cuda.is_available() else 'cpu'


def headline(message):
    buffer_len = (80 - len(message))//2 if len(message) < 80 else 0
    return "-"*buffer_len + ' ' + message + ' ' + '-'*buffer_len

def delete_directory(dir):
    if os.path.isdir(dir):
        for files in os.listdir(dir):
            path = os.path.join(dir, files)
            try:
                shutil.rmtree(path)
            except OSError:
                os.remove(path)

sys.path.append("../../")

def parse_args():
    """Parse command line arguments."""
    parser = argparse.ArgumentParser("5_Build_Track_Candidates.py")
    add_arg = parser.add_argument
    add_arg("config", nargs="?", default="pipeline_config.yaml")
    return parser.parse_args()


def label_graph(graph, score_cut=0.8, save_dir="datasets/quickstart_track_building_processed"):

    os.makedirs(save_dir, exist_ok=True)

    edge_mask = graph.scores > score_cut

    row, col = graph.edge_index[:, edge_mask]
    edge_attr = np.ones(row.size(0))

    N = graph.x.size(0)
    sparse_edges = sps.coo_matrix((edge_attr, (row.numpy(), col.numpy())), (N, N))

    _, candidate_labels = sps.csgraph.connected_components(sparse_edges, directed=False, return_labels=True)  
    graph.labels = torch.from_numpy(candidate_labels).long()

    torch.save(graph, os.path.join(save_dir, graph.event_file[-4:]))


def train(config_file="pipeline_config.yaml"):

    logging.info(headline( " Step 5: Building track candidates from the scored graph " ))

    with open(config_file) as file:
        all_configs = yaml.load(file, Loader=yaml.FullLoader)
    
    common_configs = all_configs["common_configs"]
    gnn_configs = all_configs["gnn_configs"]
    track_building_configs = all_configs["track_building_configs"]

    logging.info(headline("a) Loading scored graphs" ))

    all_graphs = []
    for subdir in ["train", "val", "test"]:
        subdir_graphs = os.listdir(os.path.join(gnn_configs["output_dir"], subdir))
        all_graphs += [torch.load(os.path.join(gnn_configs["output_dir"], subdir, graph), map_location="cpu") for graph in subdir_graphs]

    logging.info(headline( "b) Labelling graph nodes" ) )

    score_cut = track_building_configs["score_cut"]
    save_dir = track_building_configs["output_dir"]
    
    if common_configs["clear_directories"]:
        delete_directory(track_building_configs["output_dir"])

    # RUN IN SERIAL FOR NOW -->
    for graph in tqdm(all_graphs):
        label_graph(graph, score_cut=score_cut, save_dir=save_dir)



if __name__ == "__main__":

    args = parse_args()
    config_file = args.config

    train(config_file) 
