# data_processor/aggregator.py

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def aggregate_data(parsed_data_files):
    """
    Aggregates parsed simulation data from multiple files into a single dataset.
    
    Parameters:
    - parsed_data_files (list of DataFrames): List of parsed DataFrame objects
    
    Returns:
    - DataFrame containing the aggregated dataset
    """
    if not parsed_data_files:
        logging.warning("No parsed data files to aggregate.")
        return pd.DataFrame()
    
    try:
        aggregated_data = pd.concat(parsed_data_files, ignore_index=True)
        logging.info(f"Aggregated {len(parsed_data_files)} files successfully.")
        return aggregated_data
    except Exception as e:
        logging.error(f"Error during data aggregation: {e}")
        return pd.DataFrame()

def save_aggregated_data(aggregated_data, output_file):
    """
    Saves the aggregated data to a CSV file.
    
    Parameters:
    - aggregated_data (DataFrame): Aggregated data to save
    - output_file (str): Path to the output file
    """
    try:
        aggregated_data.to_csv(output_file, index=False)
        logging.info(f"Aggregated data saved to {output_file}.")
    except Exception as e:
        logging.error(f"Error saving aggregated data: {e}")
