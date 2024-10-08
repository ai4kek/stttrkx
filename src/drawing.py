#!/usr/bin/env python
# coding: utf-8
import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from .detector import detector_layout
from .math_utils import polar_to_cartesian

try:
    output_base = os.path.dirname(os.path.abspath(__file__))
except KeyError as e:
    print("Require the directory for outputs")
    print("Given by environment variable: TRKXOUTPUTDIR")
    raise e


# detector file (STT)
detector_path = os.path.join(output_base, 'stt.csv')


def Visualize_Edges (event, edges, figsize=(10,10), fig_type="pdf", save_fig=False):
    """Function to plot nodes and edges of an event."""

    # detector layout
    fig, ax = detector_layout(figsize=figsize)
    
    # get colormap for consistent track colors
    cmap = ['blue', 'red', 'green', 'orange', 'purple', 'magenta', 'black',
            'gray', 'lime', 'teal', 'navy', 'maroon', 'olive', 'indigo', 'cyan']
    
    # draw particles (event)
    unique_pids = np.unique(event.particle_id).astype(int)
    for pid in unique_pids:
        mask = (event.particle_id == pid)
        ax.scatter(event[mask].x.values, event[mask].y.values, color=cmap[pid], label=f'particle_id: {pid}')

    # draw edges (edges) 
    # for i, (source_node, target_node) in enumerate(true_edges.T):
    for (source_node, target_node) in edges.T:
        source_pos = event.loc[source_node, ['x', 'y']].values
        target_pos = event.loc[target_node, ['x', 'y']].values
        ax.plot([source_pos[0], target_pos[0]], [source_pos[1], target_pos[1]], 'k-', linewidth=0.5)

    # axis params
    evtid = event.event_id.unique()[0]
    ax.set_title('Event # {}'.format(evtid))
    ax.legend(fontsize=12, loc='best')
    fig.tight_layout()

    # save figure
    if save_fig:
        fig.savefig('event_{}.{}'.format(evtid, fig_type))


# Draw SttCSVDataReader Event:: Using Object-Oriented API
def Visualize_CSVEvent(event=None, figsize=(10,10), fig_type="pdf", save_fig=False):
    """Draw an event produced by SttCSVDataReader class."""
    
    # draw detector layout
    fig, ax = detector_layout(figsize=figsize)
    
    # get colormap for consistent track colors
    cmap = ['blue', 'red', 'green', 'orange', 'purple', 'magenta', 'black',
            'gray', 'lime', 'teal', 'navy', 'maroon', 'olive', 'indigo', 'cyan']
    
    # draw particles
    unique_pids =  np.unique(event.particle_id.values).astype(int)
    for pid in unique_pids:
        df = event.loc[event.particle_id == pid]
        ax.scatter(df.x.values, df.y.values, color=cmap[pid], label=f'particle_id: {pid}')  
    
    # axis params
    evtid = np.unique(event.event_id.values)
    ax.set_title('Event # {}'.format(evtid))
    ax.legend(fontsize=12, loc='best')
    fig.tight_layout()
    
    # save figure
    if save_fig:
        fig.savefig('event_{}.{}'.format(evtid, fig_type))
 

# Draw SttTorchDataReader Event::  Using Object-Oriented API
def Visualize_TorchEvent(event=None, figsize=(10,10), fig_type="pdf", save_fig=False):
    """Draw an event produced by SttTorchDataReader class."""
    
    # draw detector layout
    fig, ax = detector_layout(figsize=figsize)
    
    # get colormap for consistent track colors
    cmap = ['blue', 'red', 'green', 'orange', 'purple', 'magenta', 'black',
            'gray', 'lime', 'teal', 'navy', 'maroon', 'olive', 'indigo', 'cyan']
    
    # feature data
    x, y = polar_to_cartesian(r=event.x[:, 0], phi=event.x[:, 1])
    
    # draw particles
    unique_pids = np.unique(event.pid).astype(int)
    for pid in unique_pids:
        mask = (event.pid == pid)
        ax.scatter(x[mask], y[mask], color=cmap[pid], label=f'particle_id: {pid}')

    # axis params
    evtid = int(event.event_file[-10:])
    ax.set_title('Event # {}'.format(evtid))
    ax.legend(fontsize=12, loc='best')
    fig.tight_layout()
    
    # save figure
    if save_fig:
        fig.savefig('event_{}.{}'.format(evtid, fig_type))

