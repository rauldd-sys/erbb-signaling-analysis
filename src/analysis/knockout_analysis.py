import pandas as pd
import matplotlib.pyplot as plt
import copy
import numpy as np
from sympy import symbols

def perform_knockout(model, gene_name):
    """
    Performs a gene knockout by setting the specified gene to False
    
    Parameters:
    -----------
    model : BooN model
        The Boolean network model
    gene_name : str
        Name of the gene to knockout
        
    Returns:
    --------
    knocked_model : BooN model
        Model with the gene knocked out
    """
    # Create a deep copy of the model to avoid modifying the original
    knocked_model = copy.deepcopy(model)
    
    # Set the gene to always be False (knockout)
    gene_symbol = symbols(gene_name)
    knocked_model.desc[gene_symbol] = False
    
    return knocked_model

def analyze_knockouts(model, genes_to_knockout, cell_cycle_markers=None):
    """
    Analyze multiple gene knockouts and their effects on stable states
    
    Parameters:
    -----------
    model : BooN model
        The Boolean network model
    genes_to_knockout : list
        List of gene names to knockout
    cell_cycle_markers : list, optional
        List of genes that indicate cell cycle progression
        
    Returns:
    --------
    dict : Results of knockout analysis
    """
    # Default cell cycle markers if not provided
    if cell_cycle_markers is None:
        cell_cycle_markers = ['CDK2', 'CDK4', 'CDK6', 'pRB', 'Cyclin_D1', 'Cyclin_E1']
    
    results = []
    
    # First analyze the wild-type (no knockout)
    wt_stable_states = model.stable_states
    wt_result = {
        'knockout': 'None (Wild-type)',
        'stable_states_count': len(wt_stable_states),
        'cell_cycle_activity': _calculate_marker_activity(wt_stable_states, cell_cycle_markers)
    }
    results.append(wt_result)
    
    # Analyze each knockout
    for gene in genes_to_knockout:
        # Perform knockout
        ko_model = perform_knockout(model, gene)
        
        # Find stable states in knockout model
        ko_stable_states = ko_model.stable_states
        
        # Calculate cell cycle activity in knockout model
        cell_cycle_activity = _calculate_marker_activity(ko_stable_states, cell_cycle_markers)
        
        # Store results
        ko_result = {
            'knockout': gene,
            'stable_states_count': len(ko_stable_states),
            'cell_cycle_activity': cell_cycle_activity
        }
        results.append(ko_result)
    
    return {
        'results': results,
        'dataframe': pd.DataFrame(results)
    }

def _calculate_marker_activity(stable_states, markers):
    """
    Calculate the activity of cell cycle markers across stable states
    
    Parameters:
    -----------
    stable_states : list
        List of stable states
    markers : list
        List of cell cycle marker genes
        
    Returns:
    --------
    float : Average activity of markers (0-100%)
    """
    if not stable_states:
        return 0.0
        
    # Convert markers to symbols
    marker_symbols = [symbols(m) for m in markers]
    
    # Calculate activity across all stable states
    total_activity = 0
    for state in stable_states:
        # Count active markers in this state
        active_markers = sum(1 for m in marker_symbols if state.get(m, False))
        # Calculate percentage of active markers in this state
        state_activity = (active_markers / len(marker_symbols)) * 100
        total_activity += state_activity
    
    # Return average activity across all stable states
    return total_activity / len(stable_states)

def visualize_knockout_effects(knockout_results, cell_cycle_threshold=50):
    """
    Visualize the effects of gene knockouts on cell cycle progression
    
    Parameters:
    -----------
    knockout_results : dict
        Results from analyze_knockouts function
    cell_cycle_threshold : float
        Threshold percentage of marker activity that indicates cell cycle progression
        
    Returns:
    --------
    matplotlib figure
    """
    df = knockout_results['dataframe']
    
    # Create figure for visualization
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(14, 6))
    
    # Plot cell cycle activity for each knockout
    knockouts = df['knockout'].tolist()
    activity = df['cell_cycle_activity'].tolist()
    
    # Define colors based on threshold
    colors = ['green' if act >= cell_cycle_threshold else 'red' for act in activity]
    
    # Plot cell cycle activity
    ax1.bar(knockouts, activity, color=colors)
    ax1.set_title('Effect of Gene Knockouts on Cell Cycle Activity')
    ax1.set_xlabel('Knocked-out Gene')
    ax1.set_ylabel('Cell Cycle Marker Activity (%)')
    ax1.axhline(y=cell_cycle_threshold, color='orange', linestyle='--', label=f'{cell_cycle_threshold}% threshold')
    ax1.set_ylim(0, 100)
    ax1.legend()
    ax1.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    
    # Plot stable state count change
    ax2.bar(knockouts, df['stable_states_count'].tolist(), color='skyblue')
    ax2.set_title('Number of Stable States After Knockout')
    ax2.set_xlabel('Knocked-out Gene')
    ax2.set_ylabel('Number of Stable States')
    ax2.grid(axis='y', linestyle='--', alpha=0.7)
    plt.xticks(rotation=45)
    
    plt.tight_layout()
    return fig