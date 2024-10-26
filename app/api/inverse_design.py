#app/api/inverse_design.py

from machine_learning.models.cnn_model import CNNModel
from data_processor.aggregator import DataAggregator
from data_processor.validator import DataValidator

class InverseDesignAPI:
    def __init__(self):
        self.model = CNNModel()
        self.data_aggregator = DataAggregator()
        self.data_validator = DataValidator()

    def get_design_suggestions(self, target_behavior):
        # Aggregate data for model evaluation
        data = self.data_aggregator.aggregate_data()
        if not self.data_validator.validate(data):
            raise ValueError("Data validation failed")

        # Run the CNN model to predict suitable parameters
        design_params = self.model.predict(data, target_behavior)
        
        return design_params

# Example usage
if __name__ == "__main__":
    api = InverseDesignAPI()
    try:
        suggestions = api.get_design_suggestions(target_behavior="desired_output_behavior")
        print("Suggested Design Parameters:", suggestions)
    except ValueError as e:
        print("Error:", e)
