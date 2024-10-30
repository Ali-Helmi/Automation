# generator.py

import os
import json
import random
from pyaedt import Hfss, Desktop
from design_generator.utils import generate_geometry, save_design_file, calculate_deembed_distance, initialize_hfss_setup
import logging

class DesignGenerator:
    def __init__(self, template_path, output_dir="./designs", randomize=False):
        # Configure logging
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.random_seed = 42
        random.seed(self.random_seed)
        self.template_path = template_path
        self.output_dir = output_dir
        self.randomize = randomize
        self.designs = []
        self.desktop, self.hfss_app = None, None

    def load_template(self):
        try:
            with open(self.template_path, 'r') as file:
                template = json.load(file)
            return template
        except FileNotFoundError:
            logging.error(f"Template file {self.template_path} not found.")
            return {}

    def initialize_hfss(self):
        """Initialize HFSS application and create a project."""
        self.desktop, self.hfss_app = initialize_hfss_setup()

    def generate_designs(self, count=10):
        # Ensure HFSS is initialized before creating designs
        self.initialize_hfss()
        os.makedirs(self.output_dir, exist_ok=True)
        
        for i in range(count):
            design_params = self.create_random_design() if self.randomize else self.load_template()
            self.create_and_save_design(design_params, i)

        self.cleanup_hfss()

    def create_random_design(self):
        """Generate randomized design parameters."""
        return {
            "frequency": random.uniform(1e9, 10e9),
            "dimensions": {
                "width": random.uniform(0.01, 0.05),
                "height": random.uniform(0.01, 0.05)
            },
            "material": random.choice(["FR4", "Rogers", "Copper"]),
            "pattern": random.choice(["patch", "slot", "array"])
        }

    def create_and_save_design(self, params, index):
        try:
            project_name = f"metasurface_design_{index}"
            self.hfss_app.insert_design(project_name)

            # Generate geometry and assign parameters
            generate_geometry(self.hfss_app, params)
            deembed_distance = calculate_deembed_distance(params)
            initialize_hfss_setup(self.hfss_app, params, deembed_distance)

            # Save design file
            file_path = os.path.join(self.output_dir, f"{project_name}.aedt")
            save_design_file(self.hfss_app, file_path)
            self.designs.append(file_path)
            logging.info(f"Design {index} saved to {file_path}")
        except Exception as e:
            logging.error(f"Error creating design {index}: {e}")

    def cleanup_hfss(self):
        """Clean up HFSS resources."""
        if self.hfss_app:
            logging.info("Closing HFSS project.")
            self.hfss_app.close_project()
        if self.desktop:
            logging.info("Closing AEDT Desktop session.")
            self.desktop.close_desktop()

if __name__ == "__main__":
    generator = DesignGenerator(template_path="templates/template_1.json", randomize=False)
    generator.generate_designs(count=1)
