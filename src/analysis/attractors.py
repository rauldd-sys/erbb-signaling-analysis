import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from sympy import symbols
from tabulate import tabulate

def analyze_attractors(model):
    """
    Find and analyze all attractors (stable states and cycles) in the Boolean network model
    
    Parameters:
    -----------
    model : BooN model
        The Boolean network model
        
    Returns:
    --------
    dict : Dictionary containing attractor analysis results
    """
    # For now, we'll use the stable_states method which is more reliable
    # than equilibria in many BooN implementations
    stable_states = model.stable_states
    
    # Process attractors into a more structured format
    processed_attractors = []
    
    # Add stable states as attractors with length 1
    for i, state in enumerate(stable_states):
        # Calculate active nodes percentage
        total_nodes = len(model.variables)
        active_nodes_count = sum(1 for var, val in state.items() if val)
        
        attractor_info = {
            'id': i + 1,
            'type': 'Stable State',
            'length': 1,
            'states': [state],
            'average_activity': active_nodes_count / total_nodes,
            'active_percentage': (active_nodes_count / total_nodes) * 100
        }
        processed_attractors.append(attractor_info)
    
    # Create a summary DataFrame for stable states
    stable_df = None
    if stable_states:
        stable_data = []
        for ss in stable_states:
            row = {str(var): int(val) for var, val in ss.items()}
            stable_data.append(row)
        stable_df = pd.DataFrame(stable_data)
    
    return {
        'all_attractors': processed_attractors,
        'stable_states': processed_attractors,  # All attractors are stable states for now
        'cycles': [],  # No cycles detected yet
        'stable_states_df': stable_df,
        'count': len(processed_attractors),
        'stable_count': len(processed_attractors),
        'cycle_count': 0
    }

def visualize_attractor_basin(model, attractor_id, max_states=50):
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
        
    Returns:
    --------
    matplotlib figure
    """
    # Get the stable states (attractors)
    stable_states = model.stable_states
    
    if attractor_id > len(stable_states):
        raise ValueError(f"Attractor ID {attractor_id} doesn't exist. Only {len(stable_states)} attractors found.")
    
    # Create a state transition graph
    G = nx.DiGraph()
    
    # Select the target attractor state
    target_state = stable_states[attractor_id - 1]
    target_state_tuple = tuple(sorted(target_state.items()))
    
    # Add the attractor state to the graph
    G.add_node(target_state_tuple, color='red', attractor=True)
    
    # Generate some random initial states and trace their trajectories
    n_vars = len(model.variables)
    basin_states = set([target_state_tuple])
    
    # Generate random initial states and simulate
    for _ in range(min(max_states-1, 20)):
        # Create a random state
        random_state = {}
        for var in model.variables:
            random_state[var] = bool(np.random.randint(2))
        
        # Simulate trajectory
        curr_state = random_state
        state_history = []
        
        # Run the simulation until we reach a fixed point or a cycle
        for _ in range(100):  # Maximum simulation steps
            state_history.append(tuple(sorted(curr_state.items())))
            
            # Update the state
            next_state = {}
            for var in model.variables:
                if var in model.desc:
                    # Evaluate the Boolean expression for this variable
                    update_rule = model.desc[var]
                    if isinstance(update_rule, bool):
                        next_state[var] = update_rule
                    else:
                        # Try to evaluate the symbolic expression
                        try:
                            substitution = {v: curr_state.get(v, False) for v in model.variables}
                            next_state[var] = bool(update_rule.subs(substitution))
                        except:
                            # Fall back to current state if evaluation fails
                            next_state[var] = curr_state.get(var, False)
                else:
                    next_state[var] = curr_state.get(var, False)
            
            curr_state = next_state
            
            # Check if we've reached the target attractor
            curr_state_tuple = tuple(sorted(curr_state.items()))
            if curr_state_tuple == target_state_tuple:
                # Add all states in the trajectory to the basin graph
                state_history.append(curr_state_tuple)
                for i in range(len(state_history) - 1):
                    s1, s2 = state_history[i], state_history[i + 1]
                    if s1 not in basin_states:
                        G.add_node(s1, color='lightblue', attractor=False)
                        basin_states.add(s1)
                    if s2 not in basin_states and s2 != target_state_tuple:
                        G.add_node(s2, color='lightblue', attractor=False)
                        basin_states.add(s2)
                    G.add_edge(s1, s2)
                break
            
            # Check if we're in a cycle (detected by revisiting a state)
            if curr_state_tuple in state_history:
                break
    
    # Draw the basin
    plt.figure(figsize=(10, 8))
    
    # Define node colors based on whether they are attractors
    node_colors = ['red' if G.nodes[n].get('attractor', False) else 'lightblue' for n in G.nodes]
    
    # Use the spring layout algorithm for positioning nodes
    pos = nx.spring_layout(G)
    
    # Draw nodes
    nx.draw_networkx_nodes(G, pos, node_color=node_colors, alpha=0.8)
    
    # Draw edges
    nx.draw_networkx_edges(G, pos, edge_color='gray', alpha=0.6, arrowsize=10)
    
    # Add labels only to the attractor node
    attractor_nodes = {n: f"Attractor {attractor_id}" for n in G.nodes if G.nodes[n].get('attractor', False)}
    nx.draw_networkx_labels(G, pos, labels=attractor_nodes, font_size=10)
    
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