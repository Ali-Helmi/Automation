# app/app_interface.py

import argparse
from machine_learning.evaluation import evaluate_model
from machine_learning.models.cnn_model import CNNModel
from data_processor.aggregator import DataAggregator
from data_processor.validator import DataValidator
from design_generator.generator import DesignGenerator

class AppInterface:
    def __init__(self):
        self.model = CNNModel()
        self.data_aggregator = DataAggregator()
        self.data_validator = DataValidator()
        self.design_generator = DesignGenerator()

    def run(self, target_behavior):
        # Aggregate and validate data for model input
        data = self.data_aggregator.aggregate_data()
        if not self.data_validator.validate(data):
            print("Error: Data validation failed.")
            return

        # Load model and evaluate to get prediction
        design_params = evaluate_model(self.model, data, target_behavior)
        
        # Generate design based on model's prediction
        design = self.design_generator.generate(design_params)
        print(f"Generated Design: {design}")

def parse_args():
    parser = argparse.ArgumentParser(description="Inverse Design Application CLI")
    parser.add_argument(
        "--target_behavior", type=str, required=True,
        help="Specify desired electromagnetic properties for the design."
    )
    args = parser.parse_args()

    # Validate input
    if not args.target_behavior.isalnum():
        raise ValueError("Target behavior must be an alphanumeric string.")
    
    return args

if __name__ == "__main__":
    args = parse_args()
    app = AppInterface()
    app.run(args.target_behavior)
