import networkx as nx
from sympy import symbols

def identify_drug_targets(model):
    """
    Identify potential drug targets based on node influence in the network
    
    Parameters:
    -----------
    model : BooN model
        The Boolean network model
    
    Returns:
    --------
    list : List of potential drug targets with their scores
    """
    # Get all variables in the model
    variables = model.variables
    
    # Calculate the effect of freezing each node
    targets = []
    
    for var in variables:
        # Create a perturbed model where the node is knocked out (set to False)
        var_name = str(var)
        
        # Skip input nodes
        if var_name == 'EGF':
            continue
            
        # Calculate node out-degree (how many other nodes it affects)
        out_degree = sum(1 for other_var in variables 
                         if var_name in str(model.desc.get(other_var, '')))
        
        # Calculate node in-degree (how many nodes affect it)
        in_degree = len(str(model.desc.get(var, '')).split('symbols(')) - 1
        
        # Calculate a simple centrality score
        centrality_score = out_degree + in_degree
        
        targets.append({
            'node': var_name,
            'out_degree': out_degree,
            'in_degree': in_degree,
            'centrality': centrality_score,
            # Higher scores indicate better drug target candidates
            'target_score': out_degree * 2  # Weigh out-degree more
        })
    
    # Sort targets by score, descending
    targets.sort(key=lambda x: x['target_score'], reverse=True)
    
    return targets