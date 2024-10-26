# design_generator/generator.py
# Purpose: Automate the creation of ANSYS design files for metasurface unit cells.

import os
import json
import random
from pyaedt import Hfss
from design_generator.utils import generate_geometry, save_design_file

class DesignGenerator:
    def __init__(self, template_path, output_dir="./designs", randomize=False):
        self.template_path = template_path
        self.output_dir = output_dir
        self.randomize = randomize
        self.designs = []

    def load_template(self):
        with open(self.template_path, 'r') as file:
            template = json.load(file)
        return template

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
        hfss_app = Hfss()
        project_name = f"metasurface_design_{index}"
        hfss_app.new_design(project_name)

        # Generate geometry using utility function
        generate_geometry(hfss_app, params)
        
        # Save design file
        file_path = os.path.join(self.output_dir, f"{project_name}.aedt")
        save_design_file(hfss_app, file_path)

        hfss_app.save_project()
        hfss_app.close_project()

        self.designs.append(file_path)
        print(f"Design {index} saved to {file_path}")

if __name__ == "__main__":
    generator = DesignGenerator(template_path="templates/template_1.json", randomize=True)
    generator.generate_designs(count=50)
