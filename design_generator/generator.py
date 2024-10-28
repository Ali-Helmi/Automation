# design_generator/generator.py
# Purpose: Automate the creation of ANSYS design files for metasurface unit cells.

import os
import json
import random
from pyaedt import Hfss
from design_generator.utils import generate_geometry, save_design_file
import logging

class DesignGenerator:
    def __init__(self, template_path, output_dir="./designs", randomize=False):
        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.random_seed = 42  # Set for reproducible random designs; move to config for flexibility
        random.seed(self.random_seed)
        self.template_path = template_path
        self.output_dir = output_dir
        self.randomize = randomize
        self.designs = []

    def load_template(self):
        try:
            with open(self.template_path, 'r') as file:
                template = json.load(file)
            return template
        except FileNotFoundError:
            print(f"Error: Template file {self.template_path} not found.")
            return {}

    def generate_designs(self, count=10):
        os.makedirs(self.output_dir, exist_ok=True)
        for i in range(count):
            design_params = self.create_random_design() if self.randomize else self.load_template()
            self.create_and_save_design(design_params, i)

    def create_random_design(self):
        # Generate a randomized set of parameters for design
        return {
            "frequency": random.uniform(1e9, 10e9),   # Random frequency between 1 GHz and 10 GHz
            "dimensions": {
                "width": random.uniform(0.01, 0.05),  # Width in meters
                "height": random.uniform(0.01, 0.05) # Height in meters
            },
            "material": random.choice(["FR4", "Rogers", "Copper"]),
            "pattern": random.choice(["patch", "slot", "array"])
        }
        

    def create_and_save_design(self, params, index):
        try:
            with Hfss() as hfss_app:
                project_name = f"metasurface_design_{index}"
                self.hfss_app.new_design(project_name)

                # Generate geometry using utility function
                generate_geometry(self.hfss_app, params)
                
                # Save design file
                file_path = os.path.join(self.output_dir, f"{project_name}.aedt")
                save_design_file(self.hfss_app, file_path)

                self.hfss_app.save_project()
                self.designs.append(file_path)
                logging.info(f"Design {index} saved to {file_path}")
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        finally:
            if self.hfss_app:
                self.hfss_app.close_project()

if __name__ == "__main__":
    generator = DesignGenerator(template_path="templates/template_1.json", randomize=True)
    generator.generate_designs(count=50)
