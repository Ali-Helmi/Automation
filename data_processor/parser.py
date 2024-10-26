# data_processor/parser.py

import os
import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def parse_simulation_output(file_path):
    """
    Parses simulation output files to extract relevant data.
    
    Parameters:
    - file_path (str): Path to the simulation output file
    
    Returns:
    - DataFrame containing parsed data
    """
    try:
        data = pd.read_csv(file_path)  # Adjust based on output format
        processed_data = data[['Frequency', 'S11', 'S21', 'S12', 'S22']]  # Extract key parameters
        logging.info(f"Parsed {file_path} successfully.")
        return processed_data
    except Exception as e:
        logging.error(f"Error parsing {file_path}: {e}")
        return pd.DataFrame()

def parse_directory(directory_path):
    """
    Parses all files in a directory and aggregates data.
    
    Parameters:
    - directory_path (str): Path to directory with simulation output files
    
    Returns:
    - DataFrame containing aggregated data
    """
    all_data = pd.DataFrame()
    
    for file in os.listdir(directory_path):
        file_path = os.path.join(directory_path, file)
        if os.path.isfile(file_path) and file.endswith('.csv'):  # Assume CSV format
            data = parse_simulation_output(file_path)
            all_data = pd.concat([all_data, data], ignore_index=True)
    
    logging.info(f"Aggregated data from {len(all_data)} entries.")
    return all_data
