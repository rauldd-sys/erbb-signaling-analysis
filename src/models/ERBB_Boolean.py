from boon import BooN
from sympy import symbols, And, Or, Not
import matplotlib.pyplot as plt
import networkx as nx

def create_erbb_model():
    """Creates and returns the ERBB signaling network as a Boolean model"""
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
    model.desc[symbols('Cyclin_D1')] = Or(symbols('AKT1'), symbols('MEK1'), symbols('ER_alpha'), symbols('c_MYC'))
    model.desc[symbols('Cyclin_D1_star')] = And(symbols('ER_alpha'), symbols('c_MYC'), Or(symbols('AKT1'), symbols('MEK1')))
    model.desc[symbols('Cyclin_E1')] = symbols('c_MYC')
    model.desc[symbols('p21')] = And(symbols('ER_alpha'), Not(symbols('AKT1')), Not(symbols('c_MYC')), Not(symbols('CDK4')))
    model.desc[symbols('p27')] = And(symbols('ER_alpha'), Not(symbols('CDK4')), Not(symbols('CDK2')), Not(symbols('AKT1')), Not(symbols('c_MYC')))
    model.desc[symbols('pRB')] = Or(And(symbols('CDK4'), symbols('CDK6')), And(symbols('CDK4'), symbols('CDK6'), symbols('CDK2')))
    
    return model

def visualize_network(model, save_path=None):
    """Visualize the network model"""
    # First, get the interaction graph
    ig = model.interaction_graph()
    
    # Generate positions using NetworkX
    pos = nx.spring_layout(ig, seed=42)
    
    plt.figure(figsize=(12, 10))
    model.draw_IG(pos=pos)
    plt.title("ERBB Signaling Network")
    
    if save_path:
        plt.savefig(save_path)
    
    return plt.gcf()

# Create the model instance to be imported by other modules
model = create_erbb_model()

# If run as main script
if __name__ == "__main__":
    # Find stable states
    stable_states = model.stable_states
    print(f"Found {len(stable_states)} stable states:")
    for i, state in enumerate(stable_states):
        print(f"Stable state {i+1}:", state)
    
    # Visualize and save
    visualize_network(model, "results/figures/ERBB_network.png")
    plt.show()
    
    # Save the model
    model.save("data/models/ERBB_model.boon")