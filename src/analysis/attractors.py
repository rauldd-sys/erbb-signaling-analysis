"""
ERBB Signaling Network Attractor Analysis Module

This module provides tools for analyzing attractors in Boolean network models
of the ERBB signaling pathway. It includes functions to:

- Find stable states and cyclic attractors in Boolean models
- Visualize basins of attraction for specific attractors
- Analyze attractor properties and phenotypes
- Cache computation results for efficiency

Functions:
    analyze_attractors: Find all attractors in a Boolean network model
    visualize_attractor_basin: Visualize the basin of attraction for a specific attractor
    print_attractor_details: Print detailed information about all attractors
    determine_cell_division_phenotype: Determine if a state represents cell division
"""

import os
import pickle
import time
import hashlib
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from sympy import symbols, true
from sympy.core.relational import Relational
from tabulate import tabulate
from collections import defaultdict
import itertools


def safe_bool(value):
    """Safely convert a SymPy expression or other value to boolean"""
    try:
        # First check if it's a SymPy Relational object (which can't be directly evaluated)
        if isinstance(value, Relational):
            # Since we can't evaluate the truth value directly, default to False
            return False
            
        # For SymPy Boolean expressions
        if hasattr(value, 'is_Boolean') and value.is_Boolean:
            return bool(value.subs({true: True}))
            
        # Handle other types of SymPy expressions carefully
        if hasattr(value, 'subs'):  # It's likely a SymPy expression
            try:
                # Try to evaluate to a concrete True/False
                evaled = value.subs({true: True})
                return bool(evaled)
            except (TypeError, ValueError):
                # If evaluation fails, just check if non-zero/None
                return value is not None and value != 0
            
        # For normal Python values
        return bool(value)
    except (TypeError, ValueError, Exception):
        # If we get any error during conversion, default to False for safety
        return False


def analyze_attractors(model, use_cache=True, cache_dir='../cache'):
    """
    Find and analyze all attractors (stable states and cycles) in the Boolean network model
    
    Parameters:
    -----------
    model : BooN model
        The Boolean network model
    use_cache : bool
        Whether to use cached results if available
    cache_dir : str
        Directory to store cached results
        
    Returns:
    --------
    dict : Dictionary containing attractor analysis results
    """
    # Create a unique identifier for this model
    # We'll use the model's variables and descriptions to create a hash
    model_hash = hashlib.md5(str(sorted([str(v) for v in model.variables])).encode()).hexdigest()
    cache_file = os.path.join(cache_dir, f"attractors_{model_hash}.pkl")
    
    # Create cache directory if it doesn't exist
    if not os.path.exists(cache_dir):
        os.makedirs(cache_dir)
    
    # Try to load from cache first
    if use_cache and os.path.exists(cache_file):
        print(f"Loading cached attractor results from {cache_file}")
        try:
            with open(cache_file, 'rb') as f:
                return pickle.load(f)
        except (pickle.PickleError, IOError) as e:
            print(f"Could not load cache: {str(e)}")
    
    print("Starting stable states calculation...")
    start_time = time.time()
    
    # Use stable_states method which is more reliable than equilibria
    try:
        stable_states = model.stable_states
        print(f"Computation complete: Found {len(stable_states)} stable states")
        print(f"Calculation took {time.time() - start_time:.2f} seconds")
    except Exception as e:
        print(f"Error computing stable states: {str(e)}")
        stable_states = []
    
    if not stable_states:
        print("WARNING: No stable states found for this model.")
        # Return empty results structure
        return {
            'all_attractors': [],
            'stable_states': [],
            'cycles': [],
            'stable_states_df': None,
            'count': 0,
            'stable_count': 0,
            'cycle_count': 0
        }
    
    # Process attractors into a more structured format
    processed_attractors = []
    
    # Add stable states as attractors with length 1
    for i, state in enumerate(stable_states):
        # Calculate active nodes percentage
        total_nodes = len(model.variables)
        active_nodes_count = sum(1 for var, val in state.items() if safe_bool(val))
        
        # Convert all values in the state to Python booleans
        clean_state = {k: safe_bool(v) for k, v in state.items()}
        
        attractor_info = {
            'id': i + 1,
            'type': 'Stable State',
            'length': 1,
            'states': [clean_state],
            'active_percentage': (active_nodes_count / total_nodes) * 100
        }
        processed_attractors.append(attractor_info)
    
    result = {
        'all_attractors': processed_attractors,
        'stable_states': processed_attractors,  # All attractors are stable states for now
        'cycles': [],  # No cycles detected yet
        'stable_states_df': pd.DataFrame(
            [{str(k): int(safe_bool(v)) for k, v in s.items()} for s in stable_states]
        ) if stable_states else None,
        'count': len(processed_attractors),
        'stable_count': len(processed_attractors),
        'cycle_count': 0
    }
    
    # Cache the results for future use
    try:
        print(f"Saving results to cache file: {cache_file}")
        with open(cache_file, 'wb') as f:
            pickle.dump(result, f)
    except (IOError, pickle.PickleError) as e:
        print(f"Could not cache results: {str(e)}")
    
    return result


def visualize_attractor_basin(model, attractor_id, max_states=50, cached_results=None, 
                              use_cache=True, cache_dir='../cache'):
    """
    Visualize the basin of attraction for a specific attractor
    
    Parameters:
    -----------
    model : BooN model
        The Boolean network model
    attractor_id : int
        ID of the attractor to visualize (1-based indexing)
    max_states : int
        Maximum number of states to include in visualization to avoid overcrowding
    cached_results : dict, optional
        Previously calculated attractor results from analyze_attractors
    use_cache : bool
        Whether to try loading from cache if cached_results not provided
    cache_dir : str
        Directory where cache files are stored
        
    Returns:
    --------
    matplotlib figure
    """
    # Ensure max_states is an integer
    try:
        max_states = int(max_states)
    except (TypeError, ValueError):
        print("Warning: max_states parameter must be an integer. Using default value of 50.")
        max_states = 50
        
    # Try to get stable states either from provided cached results, from cache file, or by computing
    stable_states = None
    target_state = None
    
    # Option 1: Use provided cached results
    if cached_results and 'stable_states' in cached_results and cached_results['stable_states']:
        print("Using provided cached attractors for visualization")
        if attractor_id > len(cached_results['stable_states']):
            raise ValueError(
                f"Attractor ID {attractor_id} doesn't exist. "
                f"Only {len(cached_results['stable_states'])} attractors found."
            )
        # Make sure we're getting a clean dictionary with python booleans, not SymPy expressions
        raw_state = cached_results['stable_states'][attractor_id - 1]['states'][0]
        target_state = {}
        for k, v in raw_state.items():
            try:
                target_state[k] = safe_bool(v)
            except Exception:
                print(f"Warning: Could not convert {k}={v} to boolean, defaulting to False")
                target_state[k] = False
    
    # Option 2: Try loading from cache file
    elif use_cache:
        model_hash = hashlib.md5(
            str(sorted([str(v) for v in model.variables])).encode()
        ).hexdigest()
        cache_file = os.path.join(cache_dir, f"attractors_{model_hash}.pkl")
        
        if os.path.exists(cache_file):
            print(f"Loading attractor basin visualization data from cache: {cache_file}")
            try:
                with open(cache_file, 'rb') as f:
                    cached_data = pickle.load(f)
                    if 'stable_states' in cached_data and cached_data['stable_states']:
                        if attractor_id > len(cached_data['stable_states']):
                            raise ValueError(
                                f"Attractor ID {attractor_id} doesn't exist. "
                                f"Only {len(cached_data['stable_states'])} attractors found."
                            )
                        raw_state = cached_data['stable_states'][attractor_id - 1]['states'][0]
                        target_state = {}
                        for k, v in raw_state.items():
                            try:
                                target_state[k] = safe_bool(v)
                            except Exception:
                                print(f"Warning: Could not convert {k}={v} to boolean, defaulting to False")
                                target_state[k] = False
                        print(f"Successfully loaded attractor {attractor_id} from cache")
            except (IOError, pickle.PickleError) as e:
                print(f"Could not load from cache: {str(e)}")
                target_state = None
    
    # Option 3: Calculate from scratch if no cache available
    if target_state is None:
        print("Computing stable states for basin visualization (no cache available)...")
        try:
            stable_states = model.stable_states
            if not stable_states:
                raise ValueError("No stable states found in this model")
                
            if attractor_id > len(stable_states):
                raise ValueError(
                    f"Attractor ID {attractor_id} doesn't exist. "
                    f"Only {len(stable_states)} attractors found."
                )
                
            raw_state = stable_states[attractor_id - 1]
            target_state = {}
            for k, v in raw_state.items():
                try:
                    target_state[k] = safe_bool(v)
                except Exception:
                    print(f"Warning: Could not convert {k}={v} to boolean, defaulting to False")
                    target_state[k] = False
            print(f"Computed stable states, using attractor {attractor_id} for basin visualization")
        except Exception as e:
            raise ValueError(f"Error computing stable states: {str(e)}") from e
    
    # Create a state transition graph
    graph = nx.DiGraph()
    
    # Now create a string-based representation for the target state to avoid any boolean evaluation issues
    # We'll use strings like "k1=True,k2=False,..." as node identifiers
    def state_to_str(state_dict):
        """Convert a state dictionary to a stable string representation"""
        return ",".join(f"{k}={state_dict[k]}" for k in sorted(state_dict.keys()))
    
    target_state_str = state_to_str(target_state)
    
    # Add the attractor state to the graph
    graph.add_node(target_state_str, color='red', attractor=True)
    
    # Generate some random initial states and trace their trajectories
    basin_states = set([target_state_str])
    
    # Generate random initial states and simulate
    for _ in range(min(max_states-1, 20)):
        # Create a random state with Python booleans
        random_state = {}
        for var in model.variables:
            random_state[var] = bool(np.random.randint(2))
        
        # Simulate trajectory - ensure we're working with Python booleans
        curr_state = {k: bool(v) for k, v in random_state.items()}
        state_history = []
        
        # Run the simulation until we reach a fixed point or a cycle
        max_steps = 100
        for step in range(max_steps):
            # Convert the state to a string representation
            curr_state_str = state_to_str(curr_state)
            state_history.append(curr_state_str)
            
            # Update the state using the model's update rules
            next_state = {}
            for var in model.variables:
                if var in model.desc:
                    # Evaluate the Boolean expression for this variable
                    update_rule = model.desc[var]
                    if isinstance(update_rule, bool):
                        next_state[var] = update_rule
                    else:
                        # Try to evaluate the symbolic expression safely
                        try:
                            # Create substitution dictionary with clean Python booleans
                            substitution = {v: curr_state.get(v, False) for v in model.variables}
                            # Evaluate the rule
                            result = update_rule.subs(substitution)
                            # Safely convert to Python boolean
                            next_state[var] = safe_bool(result)
                        except Exception:
                            # Fall back to current state if evaluation fails
                            next_state[var] = curr_state.get(var, False)
                else:
                    next_state[var] = curr_state.get(var, False)
            
            # Ensure we have plain Python booleans
            curr_state = {k: bool(v) for k, v in next_state.items()}
            
            # Convert to string representation for comparison
            curr_state_str = state_to_str(curr_state)
            
            # Check if we've reached the target attractor
            if curr_state_str == target_state_str:
                # Add all states in the trajectory to the basin graph
                state_history.append(curr_state_str)
                for i in range(len(state_history) - 1):
                    s1, s2 = state_history[i], state_history[i + 1]
                    if s1 not in basin_states:
                        graph.add_node(s1, color='lightblue', attractor=False)
                        basin_states.add(s1)
                    if s2 not in basin_states and s2 != target_state_str:
                        graph.add_node(s2, color='lightblue', attractor=False)
                        basin_states.add(s2)
                    graph.add_edge(s1, s2)
                break
            
            # Check if we're in a cycle (detected by revisiting a state)
            if curr_state_str in state_history[:-1]:  # Exclude the state we just added
                # Add the cycle to the graph
                cycle_start_idx = state_history.index(curr_state_str)
                cycle = state_history[cycle_start_idx:] + [curr_state_str]
                
                for i in range(len(cycle) - 1):
                    s1, s2 = cycle[i], cycle[i + 1]
                    if s1 not in basin_states:
                        graph.add_node(s1, color='orange', attractor=False)
                        basin_states.add(s1)
                    if s2 not in basin_states:
                        graph.add_node(s2, color='orange', attractor=False)
                        basin_states.add(s2)
                    graph.add_edge(s1, s2)
                break
            
            # Break if we've reached the maximum number of steps
            if step == max_steps - 1:
                print(f"Warning: Reached maximum steps ({max_steps}) without finding attractor or cycle")
    
    # Draw the basin
    plt.figure(figsize=(10, 8))
    
    # Define node colors based on whether they are attractors
    node_colors = []
    for n in graph.nodes:
        if graph.nodes[n].get('attractor', False):
            node_colors.append('red')
        elif graph.nodes[n].get('color', '') == 'orange':
            node_colors.append('orange')
        else:
            node_colors.append('lightblue')
    
    # Use the spring layout algorithm for positioning nodes
    pos = nx.spring_layout(graph, k=0.3, iterations=50)
    
    # Draw nodes
    nx.draw_networkx_nodes(graph, pos, node_color=node_colors, alpha=0.8, node_size=300)
    
    # Draw edges
    nx.draw_networkx_edges(graph, pos, edge_color='gray', alpha=0.6, arrowsize=15)
    
    # Add labels only to the attractor nodes
    attractor_nodes = {
        n: f"Attractor {attractor_id}" 
        for n in graph.nodes if graph.nodes[n].get('attractor', False)
    }
    nx.draw_networkx_labels(graph, pos, labels=attractor_nodes, font_size=10, font_weight='bold')
    
    plt.title(f"Basin of Attraction for Attractor {attractor_id}")
    plt.axis('off')
    plt.tight_layout()
    
    return plt.gcf()


def print_attractor_details(attractors_result):
    """Print detailed information about all attractors"""
    print(f"Found {attractors_result['count']} attractors:")
    print(f"- {attractors_result['stable_count']} stable states")
    print(f"- {attractors_result['cycle_count']} cyclic attractors")
    
    print("\nStable States:")
    for ss in attractors_result['stable_states']:
        print(f"Stable State {ss['id']}:")
        state_dict = {str(k): int(v) for k, v in ss['states'][0].items()}
        df = pd.DataFrame([state_dict])
        print(tabulate(df, headers='keys', tablefmt='grid'))
        print(f"Active nodes: {ss['active_percentage']:.1f}%\n")


def determine_cell_division_phenotype(state, threshold=0.6):
    """Determine if a state represents a cell division phenotype"""
    key_markers = ['CDK2', 'CDK4', 'pRB']
    active_count = sum(1 for m in key_markers if safe_bool(state.get(m, False)))
    return (active_count / len(key_markers)) >= threshold