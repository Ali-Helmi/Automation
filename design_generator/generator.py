# design_generator/generator.py
# Purpose: Automate the creation of ANSYS design files for metasurface unit cells.

import os
import json
import random
from pyaedt import Hfss, Desktop
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
        self.desktop = None
        self.hfss_app = None

    def load_template(self):
        try:
            with open(self.template_path, 'r') as file:
                template = json.load(file)
            return template
        except FileNotFoundError:
            print(f"Error: Template file {self.template_path} not found.")
            return {}
    
    def initialize_hfss(self):
        """Initialize the HFSS application and set up a new project."""
        if not self.desktop:
            self.desktop = Desktop("2022.1", non_graphical=False)
        
        if not self.hfss_app:
            self.hfss_app = Hfss(
            projectname="Generated_Designs_Project",
            designname="Generated_Design",
            specified_version="2022.1",
            new_desktop_session=False
            )  # Create a new project


    def generate_designs(self, count=10):
        # Ensure HFSS is initialized before creating designs
        self.initialize_hfss()
        
        os.makedirs(self.output_dir, exist_ok=True)
        for i in range(count):
            design_params = self.create_random_design() if self.randomize else self.load_template()
            self.create_and_save_design(design_params, i)
            
        self.cleanup_hfss()

    # def create_random_design(self):
    #     # Generate a randomized set of parameters for design
    #     return {
    #         "frequency": random.uniform(1e9, 10e9),   # Random frequency between 1 GHz and 10 GHz
    #         "dimensions": {
    #             "width": random.uniform(0.01, 0.05),  # Width in meters
    #             "height": random.uniform(0.01, 0.05) # Height in meters
    #         },
    #         "material": random.choice(["FR4", "Rogers", "Copper"]),
    #         "pattern": random.choice(["patch", "slot", "array"])
    #     }
    
    
    def load_config_ranges(self):
        # Load the configuration ranges from a JSON file
        try:
            with open("templates/ranges_config.json", 'r') as file:
                config = json.load(file)
            return config
        except FileNotFoundError:
            print("Error: Configuration file not found.")
            return {}
    
    def create_random_design(self):
        # Load the configuration ranges from a JSON file
        config = self.load_config_ranges()

        # Generate a randomized set of parameters for design based on the loaded config
        return {
            "frequency": random.uniform(
                config.get("frequency", {}).get("min", 1e9), 
                config.get("frequency", {}).get("max", 10e9)
            ),
            "dimensions": {
                "width": random.uniform(
                    config.get("dimensions", {}).get("width", {}).get("min", 0.01), 
                    config.get("dimensions", {}).get("width", {}).get("max", 0.05)
                ),
                "height": random.uniform(
                    config.get("dimensions", {}).get("height", {}).get("min", 0.01), 
                    config.get("dimensions", {}).get("height", {}).get("max", 0.05)
                ),
                "thickness": random.uniform(
                    config.get("dimensions", {}).get("thickness", {}).get("min", 0.001), 
                    config.get("dimensions", {}).get("thickness", {}).get("max", 0.01)
                )
            },
            "material": {
                "substrate_material": random.choice(
                    config.get("material", {}).get("substrate_material", ["FR4_epoxy", "Rogers"])
                ),
                "metal_material": config.get("material", {}).get("metal_material", "Copper"),
                "radiation_material": config.get("material", {}).get("radiation_material", "vacuum")
            },
            "pattern": {
                "type": random.choice(
                    config.get("pattern", {}).get("type", ["patch", "slot"])
                ),
                "geometry": random.choice(
                    config.get("pattern", {}).get("geometry", ["square", "circular"])
                )
            },
            # Add frequency sweep if it exists in config
            "frequency_sweep": config.get("frequency_sweep", {
                "start": 5e9,
                "stop": 15e9,
                "points": 501
            }),
            # Add boundary conditions if it exists in config
            "boundary_conditions": config.get("boundary_conditions", {
                "type": "Floquet Periodic",
                "excitation": {
                    "type": "Plane Wave",
                    "angle_of_incidence": 0
                }
            }),
            # Static parameters with fallback defaults
            "cell_width": config.get("cell_width", "2.5mm"),
            "patch_thickness": config.get("patch_thickness", "0.017mm"),
            "patch_gapLength": config.get("patch_gapLength", "0.3mm"),
            "patch_gapWidth": config.get("patch_gapWidth", "0.2mm"),
            "substrate_height": config.get("substrate_height", "0.25mm"),
            "wire_length": config.get("wire_length", "2.5mm"),
            "wire_width": config.get("wire_width", "0.14mm"),
            "rad_length": config.get("rad_length", "2.51mm"),
            "rad_width": config.get("rad_width", "2.51mm"),
            "rad_height": config.get("rad_height", "2.51mm")
        }
        

    def create_and_save_design(self, params, index):
        try:
            if not self.hfss_app:
                raise RuntimeError("HFSS application is not initialized.")

            for key, value in params.items():
                try:
                    # Convert parameters with units to their numerical values before assigning
                    if isinstance(value, str) and value.endswith(('mm', 'GHz')):
                        numeric_value = float(value[:-2])
                        self.hfss_app[key] = numeric_value
                    elif isinstance(value, (float, int)):
                        self.hfss_app[key] = value
                    else:
                        raise ValueError(f"Invalid type or unit for parameter {key}: {value}")
                except Exception as e:
                    logging.error(f"Failed to set HFSS parameter {key} with value {value}: {e}")


                
            project_name = f"metasurface_design_{index}"
            self.hfss_app.insert_design(project_name)

            # Generate geometry using utility function
            generate_geometry(self.hfss_app, params)
            assign_ports_and_boundaries(self.hfss_app, params)
            
            # Save design file
            file_path = os.path.join(self.output_dir, f"{project_name}.aedt")
            save_design_file(self.hfss_app, file_path)

            #self.hfss_app.save_project(file_path)
            self.designs.append(file_path)
            logging.info(f"Design {index} saved to {file_path}")
        except FileNotFoundError as e:
            logging.error(f"File not found: {e}")
        except Exception as e:
            logging.error(f"An unexpected error occurred: {e}")
        finally:
            if self.hfss_app:
                # Avoid closing the project prematurely; consider keeping it open if running multiple designs
                logging.info("Design creation complete for index: {}".format(index))

    def cleanup_hfss(self):
        """Clean up and close the HFSS project and desktop session."""
        if self.hfss_app:
            logging.info("Closing HFSS project.")
            self.hfss_app.close_project()
        
        if self.desktop:
            logging.info("Closing AEDT Desktop session.")
            self.desktop.close_desktop()

if __name__ == "__main__":
    generator = DesignGenerator(template_path="templates/template_1.json", randomize=False)
    generator.generate_designs(count=1)
