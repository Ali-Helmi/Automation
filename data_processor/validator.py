# data_processor/validator.py

import pandas as pd
import logging

logging.basicConfig(level=logging.INFO)

def validate_data(data: pd.DataFrame) -> bool:
    """
    Validates the input data for missing values, data types, and expected ranges.

    Parameters:
    - data (pd.DataFrame): The DataFrame to validate

    Returns:
    - bool: True if data is valid, False otherwise
    """
    try:
        # Check for missing values
        if data.isnull().any().any():
            logging.warning("Data contains missing values.")
            return False
        
        # Check for specific column data types and ranges
        expected_columns = {
            "frequency": (float, (1e9, 1e12)),  # Hz range, adjust as necessary
            "gain": (float, (-50, 50)),        # dB range, adjust as necessary
            "efficiency": (float, (0, 1))      # Efficiency in range [0,1]
        }
        
        for column, (dtype, valid_range) in expected_columns.items():
            if column not in data.columns:
                logging.error(f"Missing expected column: {column}")
                return False
            if not pd.api.types.is_float_dtype(data[column]):
                logging.error(f"Column {column} has incorrect data type.")
                return False
            if not ((data[column] >= valid_range[0]) & (data[column] <= valid_range[1])).all():
                logging.error(f"Column {column} has values outside the expected range.")
                return False

        logging.info("Data validation successful.")
        return True
    except Exception as e:
        logging.error(f"Data validation failed: {e}")
        return False
