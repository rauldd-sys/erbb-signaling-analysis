# Contents for src/models/network_visualization.py

import matplotlib.pyplot as plt
import networkx as nx

def draw_interaction_graph(model):
    """
    Draws the interaction graph of the ERBB signaling network.

    Parameters:
    model: The Boolean network model containing the nodes and their interactions.

    Returns:
    None
    """
    ig = model.draw_IG()
    pos = nx.spring_layout(ig, seed=42)  # Using spring layout for better visualization
    nx.draw(ig, pos, with_labels=True, node_size=700, node_color='lightblue', font_size=10, font_weight='bold')
    plt.title("ERBB Signaling Network Interaction Graph")
    plt.tight_layout()
    plt.show()

# Contents for src/models/controllability.py

from boon import BooN

def analyze_controllability(model):
    """
    Performs controllability analysis on the ERBB signaling network.

    Parameters:
    model: The Boolean network model to analyze.

    Returns:
    dict: A dictionary containing potential gene freezes and their effects.
    """
    frozen_vars = model.variables  # Get all variables in the model
    results = {}

    for var in frozen_vars:
        # Analyze the effect of freezing each variable
        model_copy = model.copy()
        model_copy.desc[var] = False  # Freeze the variable
        stable_states = model_copy.stable_states
        results[var] = stable_states

    return results

# Contents for src/analysis/stable_states.py

import pandas as pd
from sympy import symbols

def analyze_stable_states(model):
    """
    Analyze stable states of the Boolean network model
    
    Parameters:
    -----------
    model : BooN model
        The Boolean network model
    
    Returns:
    --------
    dict : Analysis results of stable states
    """
    # Get stable states from the model
    stable_states = model.stable_states
    
    # Prepare output in a structured format
    results = []
    
    for i, state in enumerate(stable_states):
        # Extract key information from each stable state
        state_info = {
            'id': i,
            'name': f"State {i+1}",
            'value': sum(1 for v in state.values() if v),  # Count active nodes as value
            'active_nodes': [str(node) for node, value in state.items() if value],
            'inactive_nodes': [str(node) for node, value in state.items() if not value],
            'state': state
        }
        
        # Calculate percentage of active nodes
        total_nodes = len(state)
        active_count = sum(1 for v in state.values() if v)
        state_info['active_percentage'] = (active_count / total_nodes) * 100
        
        results.append(state_info)
    
    # Create a summary DataFrame as well
    df = pd.DataFrame({str(k): [v for v in state.values()] 
                      for k, state in zip(range(len(stable_states)), stable_states)})
    
    # Store both the structured results and the DataFrame
    return {
        'states': results,
        'dataframe': df,
        'count': len(stable_states)
    }

def get_node_stability(model, node_name):
    """
    Analyze how stable a specific node is across all stable states
    
    Parameters:
    -----------
    model : BooN model
        The Boolean network model
    node_name : str
        Name of the node to analyze
    
    Returns:
    --------
    dict : Stability information for the node
    """
    stable_states = model.stable_states
    node_symbol = symbols(node_name)
    
    # Count in how many states the node is active
    active_count = sum(1 for state in stable_states if state.get(node_symbol, False))
    
    return {
        'node': node_name,
        'active_count': active_count,
        'total_states': len(stable_states),
        'active_percentage': (active_count / len(stable_states)) * 100 if stable_states else 0
    }

# Note: Each of these files is designed to encapsulate specific functionalities related to the ERBB signaling network analysis.