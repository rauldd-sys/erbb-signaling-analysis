import pandas as pd
import numpy as np
from sympy import symbols

def analyze_biomarkers(model):
    """
    Analyze potential biomarkers based on node stability and influence
    
    Parameters:
    -----------
    model : BooN model
        The Boolean network model
    
    Returns:
    --------
    dict : Dictionary of biomarker analysis results
    """
    # Get stable states
    stable_states = model.stable_states
    
    biomarkers = []
    
    # Calculate stability of each node across stable states
    for var in model.variables:
        var_name = str(var)
        
        # Count active states
        active_count = sum(1 for state in stable_states if state.get(var, False))
        active_percentage = (active_count / len(stable_states)) * 100 if stable_states else 0
        
        # Very stable (always on or always off) nodes can be good biomarkers
        stability_score = max(active_percentage, 100 - active_percentage)
        
        # Nodes that determine many other nodes' states are potentially good biomarkers
        influence_score = sum(1 for other_var in model.variables 
                            if var_name in str(model.desc.get(other_var, '')))
        
        # Calculate a combined biomarker score
        biomarker_score = (stability_score * 0.6) + (influence_score * 0.4)
        
        biomarkers.append({
            'node': var_name,
            'stability_score': stability_score,
            'influence_score': influence_score,
            'biomarker_score': biomarker_score
        })
    
    # Sort biomarkers by score, descending
    biomarkers.sort(key=lambda x: x['biomarker_score'], reverse=True)
    
    # Group biomarkers by quality
    excellent = [b for b in biomarkers if b['biomarker_score'] > 80]
    good = [b for b in biomarkers if 60 <= b['biomarker_score'] <= 80]
    moderate = [b for b in biomarkers if 40 <= b['biomarker_score'] < 60]
    poor = [b for b in biomarkers if b['biomarker_score'] < 40]
    
    return {
        'all_biomarkers': biomarkers,
        'excellent': excellent,
        'good': good,
        'moderate': moderate,
        'poor': poor
    }