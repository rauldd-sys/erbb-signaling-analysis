#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Generate model prediction dictionaries from phenotype control results.
This script systematically analyzes model predictions from CSV files and creates
dictionaries showing expected vs. actual model behavior.
"""

import os
import pandas as pd
import json
import argparse
from typing import Dict, Any, List, Tuple

def get_model_predictions(model_phenotype_file: str, expectations_file: str) -> Tuple[Dict[str, Dict[str, bool]], List[str]]:
    """
    Generate a dictionary of model predictions from phenotype control files.
    
    Args:
        model_phenotype_file: Path to the model phenotype control CSV file
        expectations_file: Path to the expectations phenotype control results
        
    Returns:
        A tuple containing:
        - Dictionary of model predictions with discrepancy annotations
        - List of perturbations with mismatches
    """
    # Read the phenotype control files
    model_df = pd.read_csv(model_phenotype_file)
    expected_df = pd.read_csv(expectations_file)
    
    # Create the model predictions dictionary
    model_predictions = {}
    mismatch_perturbations = []
    
    # Process perturbations from the expectations file
    for _, row in expected_df.iterrows():
        perturbation = row['Perturbation']
        
        # Extract expected and model predictions
        expected_prolif = str(row['Expected_Proliferation']).lower() == 'true'
        model_prolif = str(row['Model_Proliferation']).lower() == 'true'
        expected_apop = str(row['Expected_Apoptosis']).lower() == 'true'
        model_apop = str(row['Model_Apoptosis']).lower() == 'true'
        
        # Determine if this perturbation has mismatches
        has_mismatch = (expected_prolif != model_prolif) or (expected_apop != model_apop)
        
        # Create entry in the dictionary
        model_predictions[perturbation] = {
            'Proliferation': model_prolif,
            'Apoptosis': model_apop
        }
        
        # Add to mismatch list if needed
        if has_mismatch:
            mismatch_perturbations.append(perturbation)
    
    return model_predictions, mismatch_perturbations


def get_node_status_from_model_file(model_file: str) -> Dict[str, Dict[str, bool]]:
    """
    Extract proliferation and apoptosis status directly from a model phenotype control file.
    
    Args:
        model_file: Path to the model phenotype control CSV
        
    Returns:
        Dictionary of perturbation states
    """
    try:
        # Read the model file
        model_df = pd.read_csv(model_file)
        
        # Create the results dictionary
        results = {}
        
        # Extract knockout (KO) perturbations
        for _, row in model_df.iterrows():
            node = row.get('node', None)
            if node is None or node == 'Unperturbed':
                continue
                
            fixed_value = row.get('fixed_value', None)
            allows_cell_cycle = row.get('allows_cell_cycle', False)
            causes_arrest = row.get('causes_arrest', False)
            
            # Only process knockouts (where fixed_value is False)
            if fixed_value is False:
                perturbation = f"{node}_KO"
                results[perturbation] = {
                    'Proliferation': allows_cell_cycle,
                    'Apoptosis': False  # Simplified assumption
                }
            # Process overexpression (where fixed_value is True)
            elif fixed_value is True and node in ['c_MYC']:
                perturbation = f"{node}_OE"
                results[perturbation] = {
                    'Proliferation': allows_cell_cycle,
                    'Apoptosis': False  # Simplified assumption
                }
                
        return results
    except Exception as e:
        print(f"Error processing model file: {e}")
        return {}


def create_model_comparison_dictionary(
    model_predictions: Dict[str, Dict[str, bool]], 
    expected_df: pd.DataFrame
) -> Dict[str, Dict[str, bool]]:
    """
    Create a formatted dictionary with annotations about prediction mismatches.
    
    Args:
        model_predictions: Dictionary of model predictions
        expected_df: DataFrame with expected results
        
    Returns:
        Annotated dictionary with mismatch comments
    """
    annotated_predictions = {}
    
    for _, row in expected_df.iterrows():
        perturbation = row['Perturbation']
        if perturbation not in model_predictions:
            continue
            
        expected_prolif = str(row['Expected_Proliferation']).lower() == 'true'
        expected_apop = str(row['Expected_Apoptosis']).lower() == 'true'
        
        model_prolif = model_predictions[perturbation]['Proliferation']
        model_apop = model_predictions[perturbation]['Apoptosis']
        
        # Create the prediction entry
        prediction_entry = {
            'Proliferation': model_prolif,
            'Apoptosis': model_apop
        }
        
        # Check for mismatches and add comments
        has_mismatch = False
        if expected_prolif != model_prolif or expected_apop != model_apop:
            has_mismatch = True
            
        # Add the entry to the dictionary with comment if needed
        annotated_predictions[perturbation] = prediction_entry
        
    return annotated_predictions


def format_dictionary_output(model_dict: Dict[str, Dict[str, bool]], mismatches: List[str]) -> str:
    """
    Format the dictionary output to a nicely formatted string with comments.
    
    Args:
        model_dict: Dictionary of model predictions
        mismatches: List of perturbations with mismatches
        
    Returns:
        Formatted string representation
    """
    output = "model_predictions = {\n"
    
    for perturbation, predictions in model_dict.items():
        output += f"    '{perturbation}': {predictions},"
        
        if perturbation in mismatches:
            output += "  # Doesn't match expectation"
            
        output += "\n"
        
    output += "}\n"
    return output


def main():
    """Main function to run the script."""
    parser = argparse.ArgumentParser(description='Generate model prediction dictionaries from phenotype control results')
    parser.add_argument('--model', choices=['original', 'refined'], default='original',
                        help='Which model to analyze (original or refined)')
    args = parser.parse_args()
    
    # Set up file paths
    project_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
    results_dir = os.path.join(project_dir, 'results')
    
    expectations_file = os.path.join(results_dir, 'phenotype_control_results.csv')
    
    if args.model == 'original':
        model_file = os.path.join(results_dir, 'original_model_phenotype_control.csv')
        output_file = os.path.join(results_dir, 'original_model_predictions.py')
    else:
        model_file = os.path.join(results_dir, 'refined_model_phenotype_control.csv')
        output_file = os.path.join(results_dir, 'refined_model_predictions.py')
    
    # Read the expectations file
    expected_df = pd.read_csv(expectations_file)
    
    # Get predictions directly from model file
    model_predictions = get_node_status_from_model_file(model_file)
    
    # Annotate the predictions
    annotated_predictions = create_model_comparison_dictionary(model_predictions, expected_df)
    
    # Get the list of mismatches
    mismatches = []
    for perturbation in annotated_predictions:
        model_values = annotated_predictions[perturbation]
        expected_row = expected_df[expected_df['Perturbation'] == perturbation]
        
        if not expected_row.empty:
            expected_prolif = str(expected_row['Expected_Proliferation'].values[0]).lower() == 'true'
            expected_apop = str(expected_row['Expected_Apoptosis'].values[0]).lower() == 'true'
            
            if (expected_prolif != model_values['Proliferation']) or (expected_apop != model_values['Apoptosis']):
                mismatches.append(perturbation)
    
    # Format the output
    output = format_dictionary_output(annotated_predictions, mismatches)
    
    # Write to file
    with open(output_file, 'w') as f:
        f.write(f"# {args.model.capitalize()} model predictions\n")
        f.write("# This file was automatically generated\n\n")
        f.write(output)
    
    print(f"Generated {args.model} model predictions in {output_file}")
    print(f"Found {len(mismatches)} mismatches between expected and model predictions:")
    for mismatch in mismatches:
        print(f"  - {mismatch}")


if __name__ == "__main__":
    main()