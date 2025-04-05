import sys
import os

# Add the parent directory of this project to the path to find BooN properly
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

try:
    from boon import BooN
except ImportError:
    print("BooN module not found in default path, trying alternative paths...")
    # Try different paths to locate BooN
    possible_paths = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../BooN-1.60')),
        os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')),
        '/Users/raulduran/Documents/M1_GENIOMHE/Term_3/ModelingSystems/Project/BooN-1.60'
    ]
    
    for path in possible_paths:
        if path not in sys.path:
            print(f"Adding path: {path}")
            sys.path.append(path)
    
    try:
        from boon import BooN
        print(f"BooN module found and imported successfully!")
    except ImportError as e:
        print(f"Failed to import BooN: {str(e)}")
        # Create a minimal BooN class as fallback
        class BooN:
            def __init__(self):
                self.desc = {}
                self.variables = []
                print("Warning: Using placeholder BooN class!")
            
            def copy(self):
                return BooN()
            
            @property
            def interaction_graph(self):
                import networkx as nx
                return nx.DiGraph()
                
            def save(self, path):
                print(f"Placeholder save to {path}")

from sympy import symbols, And, Or, Not
import matplotlib.pyplot as plt
import networkx as nx

def create_erbb_original_model():
    """Creates and returns the ERBB signaling network with original Cyclin_D1 rule as a Boolean model"""
    model = BooN()

    # Define the rules for each node in the network
    # The BooN library uses sympy for boolean logic expressions
    model.desc[symbols('EGF')] = symbols('EGF')  # Input node stays the same
    model.desc[symbols('ERBB1')] = symbols('EGF')
    model.desc[symbols('ERBB2')] = symbols('EGF')
    model.desc[symbols('ERBB3')] = symbols('EGF')
    model.desc[symbols('ERBB1_2')] = And(symbols('ERBB1'), symbols('ERBB2'))
    model.desc[symbols('ERBB1_3')] = And(symbols('ERBB1'), symbols('ERBB3'))
    model.desc[symbols('ERBB2_3')] = And(symbols('ERBB2'), symbols('ERBB3'))
    model.desc[symbols('ER_alpha')] = Or(symbols('AKT1'), symbols('MEK1'))
    model.desc[symbols('IGF1R')] = And(Or(symbols('ER_alpha'), symbols('AKT1')), Not(symbols('ERBB2_3')))
    model.desc[symbols('c_MYC')] = Or(symbols('AKT1'), symbols('MEK1'), symbols('ER_alpha'))
    model.desc[symbols('AKT1')] = Or(symbols('ERBB1'), symbols('ERBB1_2'), symbols('ERBB1_3'), symbols('ERBB2_3'), symbols('IGF1R'))
    model.desc[symbols('MEK1')] = Or(symbols('ERBB1'), symbols('ERBB1_2'), symbols('ERBB1_3'), symbols('ERBB2_3'), symbols('IGF1R'))
    model.desc[symbols('CDK2')] = And(symbols('Cyclin_E1'), Not(symbols('p21')), Not(symbols('p27')))
    model.desc[symbols('CDK4')] = And(symbols('Cyclin_D1'), Not(symbols('p21')), Not(symbols('p27')))
    model.desc[symbols('CDK6')] = symbols('Cyclin_D1')
    
    # Original loose rule for Cyclin_D1
    model.desc[symbols('Cyclin_D1')] = Or(symbols('AKT1'), symbols('MEK1'), symbols('ER_alpha'), symbols('c_MYC'))
    
    model.desc[symbols('Cyclin_E1')] = symbols('c_MYC')
    model.desc[symbols('p21')] = And(symbols('ER_alpha'), Not(symbols('AKT1')), Not(symbols('c_MYC')), Not(symbols('CDK4')))
    model.desc[symbols('p27')] = And(symbols('ER_alpha'), Not(symbols('CDK4')), Not(symbols('CDK2')), Not(symbols('AKT1')), Not(symbols('c_MYC')))
    model.desc[symbols('pRB')] = Or(And(symbols('CDK4'), symbols('CDK6')), And(symbols('CDK4'), symbols('CDK6'), symbols('CDK2')))
    
    return model

def create_erbb_refined_model():
    """Creates and returns the ERBB signaling network with refined Cyclin_D1 rule as a Boolean model"""
    model = BooN()

    # Define the rules for each node in the network
    # The BooN library uses sympy for boolean logic expressions
    model.desc[symbols('EGF')] = symbols('EGF')  # Input node stays the same
    model.desc[symbols('ERBB1')] = symbols('EGF')
    model.desc[symbols('ERBB2')] = symbols('EGF')
    model.desc[symbols('ERBB3')] = symbols('EGF')
    model.desc[symbols('ERBB1_2')] = And(symbols('ERBB1'), symbols('ERBB2'))
    model.desc[symbols('ERBB1_3')] = And(symbols('ERBB1'), symbols('ERBB3'))
    model.desc[symbols('ERBB2_3')] = And(symbols('ERBB2'), symbols('ERBB3'))
    model.desc[symbols('ER_alpha')] = Or(symbols('AKT1'), symbols('MEK1'))
    model.desc[symbols('IGF1R')] = And(Or(symbols('ER_alpha'), symbols('AKT1')), Not(symbols('ERBB2_3')))
    model.desc[symbols('c_MYC')] = Or(symbols('AKT1'), symbols('MEK1'), symbols('ER_alpha'))
    model.desc[symbols('AKT1')] = Or(symbols('ERBB1'), symbols('ERBB1_2'), symbols('ERBB1_3'), symbols('ERBB2_3'), symbols('IGF1R'))
    model.desc[symbols('MEK1')] = Or(symbols('ERBB1'), symbols('ERBB1_2'), symbols('ERBB1_3'), symbols('ERBB2_3'), symbols('IGF1R'))
    model.desc[symbols('CDK2')] = And(symbols('Cyclin_E1'), Not(symbols('p21')), Not(symbols('p27')))
    model.desc[symbols('CDK4')] = And(symbols('Cyclin_D1'), Not(symbols('p21')), Not(symbols('p27')))
    model.desc[symbols('CDK6')] = symbols('Cyclin_D1')
    
    # Refined stricter rule for Cyclin_D1
    model.desc[symbols('Cyclin_D1')] = And(symbols('ER_alpha'), symbols('c_MYC'), Or(symbols('AKT1'), symbols('MEK1')))
    
    model.desc[symbols('Cyclin_E1')] = symbols('c_MYC')
    model.desc[symbols('p21')] = And(symbols('ER_alpha'), Not(symbols('AKT1')), Not(symbols('c_MYC')), Not(symbols('CDK4')))
    model.desc[symbols('p27')] = And(symbols('ER_alpha'), Not(symbols('CDK4')), Not(symbols('CDK2')), Not(symbols('AKT1')), Not(symbols('c_MYC')))
    model.desc[symbols('pRB')] = Or(And(symbols('CDK4'), symbols('CDK6')), And(symbols('CDK4'), symbols('CDK6'), symbols('CDK2')))
    
    return model

def visualize_network(model, save_path=None, title="ERBB Signaling Network"):
    """Visualize the network model"""
    # First, get the interaction graph
    ig = model.interaction_graph
    
    # Generate positions using NetworkX
    pos = nx.spring_layout(ig, seed=42)
    
    plt.figure(figsize=(12, 10))
    
    # Define node colors based on function
    node_colors = []
    for node in ig.nodes():
        node_str = str(node)
        if node_str in ['ERBB1', 'ERBB2', 'ERBB3', 'ERBB1_2', 'ERBB1_3', 'ERBB2_3', 'IGF1R', 'ER_alpha']:
            color = 'lightcoral'  # Receptors
        elif node_str in ['AKT1', 'MEK1', 'c_MYC', 'EGF']:
            color = 'lightskyblue'  # Signaling molecules
        elif node_str in ['CDK2', 'CDK4', 'CDK6', 'Cyclin_D1', 'Cyclin_E1', 'pRB']:
            color = 'lightgreen'  # Cell cycle activators
        elif node_str in ['p21', 'p27']:
            color = 'lightyellow'  # Cell cycle inhibitors
        else:
            color = 'lightgray'  # Other components
        node_colors.append(color)
    
    # Draw nodes with colors
    nx.draw_networkx_nodes(ig, pos, node_color=node_colors, node_size=2000, alpha=0.8)
    
    # Draw edges
    nx.draw_networkx_edges(ig, pos, edge_color='gray', width=1.5, arrowsize=20, alpha=0.7)
    
    # Draw labels
    nx.draw_networkx_labels(ig, pos, font_size=10, font_weight='bold')
    
    plt.title(title, fontsize=16)
    plt.axis('off')
    
    if save_path:
        plt.savefig(save_path, dpi=300, bbox_inches='tight')
    
    return plt.gcf()

def compare_models():
    """Compare the original and refined models side by side"""
    original = create_erbb_original_model()
    refined = create_erbb_refined_model()
    
    print("Original Model - Cyclin D1 Rule:")
    print(f"Cyclin_D1 = {original.desc[symbols('Cyclin_D1')]}")
    
    print("\nRefined Model - Cyclin D1 Rule:")
    print(f"Cyclin_D1 = {refined.desc[symbols('Cyclin_D1')]}")
    
    # Compare stable states
    try:
        original_states = original.stable_states
        refined_states = refined.stable_states
        
        print(f"\nOriginal Model has {len(original_states)} stable states")
        print(f"Refined Model has {len(refined_states)} stable states")
    except Exception as e:
        print(f"Error calculating stable states: {str(e)}")
    
    return original, refined

# Explicitly export these names
__all__ = ['original_model', 'refined_model', 'model', 'visualize_network', 'compare_models']

# Initialize the models - wrap in try/except to ensure they're always created
try:
    # Create both model instances to be imported by other modules
    print("Initializing ERBB signaling models...")
    original_model = create_erbb_original_model()
    refined_model = create_erbb_refined_model()

    # Default model to use (refined version)
    model = refined_model
    print("Models initialized successfully!")
except Exception as e:
    print(f"Error initializing models: {str(e)}")
    # Provide default empty models as fallback
    original_model = BooN()
    refined_model = BooN()
    model = refined_model

# If run as main script
if __name__ == "__main__":
    try:
        # Compare the models
        original_model, refined_model = compare_models()
        
        # Visualize both models
        plt.figure(figsize=(16, 8))
        
        plt.subplot(1, 2, 1)
        visualize_network(original_model, "data/models/ERBB_original_network.png", 
                         "Original ERBB Network (Loose Cyclin D1 Rule)")
        
        plt.subplot(1, 2, 2)
        visualize_network(refined_model, "data/models/ERBB_refined_network.png", 
                         "Refined ERBB Network (Strict Cyclin D1 Rule)")
        
        plt.tight_layout()
        plt.show()
        
        # Create directories if they don't exist
        os.makedirs("data/models", exist_ok=True)
        
        # Save the models
        original_model.save("data/models/ERBB_original_model.boon")
        refined_model.save("data/models/ERBB_refined_model.boon")
    except Exception as e:
        print(f"Error during execution: {str(e)}")