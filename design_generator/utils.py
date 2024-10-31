import json
import logging

def setup_logger():
    logger = logging.getLogger("HFSSGenerator")
    logger.setLevel(logging.INFO)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

def load_template(filepath):
    try:
        with open(filepath, "r") as file:
            data = json.load(file)
        return data
    except Exception as e:
        print(f"Error loading template: {e}")
        return None
