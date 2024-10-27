# machine_learning/datasets.py
import numpy as np
import tensorflow as tf
from sklearn.model_selection import train_test_split
import pandas as pd

class DatasetHandler:
    def __init__(self, data_path, validation_split=0.2, test_split=0.1):
        self.data_path = data_path
        self.validation_split = validation_split
        self.test_split = test_split

    def load_data(self):
        # Load data from the specified path
        try:
            data = pd.read_csv(self.data_path)
            features = data.drop(columns=['label']).values
            labels = data['label'].values
            return features, labels
        except Exception as e:
            print(f"Error loading data: {e}")
            return None, None

    def preprocess_data(self, features):
        # Normalize features to be between 0 and 1
        return features / np.max(features)

    def get_train_val_test_split(self):
        features, labels = self.load_data()
        if features is None:
            return None, None, None, None, None, None

        features = self.preprocess_data(features)
        x_train, x_temp, y_train, y_temp = train_test_split(features, labels, test_size=(self.validation_split + self.test_split))
        val_split_adjusted = self.validation_split / (self.validation_split + self.test_split)
        x_val, x_test, y_val, y_test = train_test_split(x_temp, y_temp, test_size=val_split_adjusted)

        return x_train, y_train, x_val, y_val, x_test, y_test

if __name__ == "__main__":
    dataset_handler = DatasetHandler(data_path="data/simulation_data.csv")
    x_train, y_train, x_val, y_val, x_test, y_test = dataset_handler.get_train_val_test_split()
