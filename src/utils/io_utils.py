import os
import pandas as pd
import matplotlib.pyplot as plt
import sys
import pickle

sys.path.append(os.path.abspath('..'))

# Define missing IO utility functions
def save_model(model, filepath):
    """Save a model to a file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    with open(filepath, 'wb') as f:
        pickle.dump(model, f)
    print(f"Model saved to {filepath}")
    
def load_model(filepath):
    """Load a model from a file."""
    with open(filepath, 'rb') as f:
        return pickle.load(f)
    
def save_visualization(figure, filepath):
    """Save a matplotlib figure to a file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    figure.savefig(filepath)
    print(f"Figure saved to {filepath}")
    
def save_results(data, filepath):
    """Save results to a CSV file."""
    os.makedirs(os.path.dirname(filepath), exist_ok=True)
    data.to_csv(filepath, index=False)
    print(f"Results saved to {filepath}")