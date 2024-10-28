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
        
    def initialize_parameters_and_setup(self, params):
        """Assign parameters and create a setup for the design."""
        # Assign all necessary parameters
        self.hfss_app["cell_width"] = "2.5mm"
        self.hfss_app["patch_outerWidth1"] = "2.2mm"
        self.hfss_app["patch_outerWidth2"] = "1.5mm"
        self.hfss_app["patch_innerWidth1"] = "1.8mm"
        self.hfss_app["patch_innerWidth2"] = "1.1mm"
        self.hfss_app["patch_gapLength"] = "0.3mm"
        self.hfss_app["patch_gapWidth"] = "0.2mm"
        self.hfss_app["substrate_height"] = "0.25mm"
        self.hfss_app["wire_length"] = "2.5mm"
        self.hfss_app["wire_width"] = "0.14mm"
        self.hfss_app["rad_length"] = "2.51mm"
        self.hfss_app["rad_width"] = "2.51mm"
        self.hfss_app["rad_height"] = "2.51mm"
        self.hfss_app["lower_frequency"] = "5GHz"
        self.hfss_app["upper_frequency"] = "15GHz"
        self.hfss_app["solution_frequency"] = "10GHz"
        self.hfss_app["patch_thickness"] = "0.017mm"
        self.hfss_app["wavelength"] = "29.97925mm"

        # Assign Setup and Sweep
        setup = self.hfss_app.create_setup("Setup1")
        setup.props["Frequency"] = self.hfss_app["solution_frequency"]
        setup["MaximumPasses"] = 21
        self.hfss_app.create_linear_count_sweep(
            setupname="Setup1", unit="GHz", freqstart=5, freqstop=15,
            num_of_freq_points=501, sweepname="sweep1",
            sweep_type="Interpolating", save_fields=False
        )



    def create_and_save_design(self, params, index):
        try:
            if not self.hfss_app:
                raise RuntimeError("HFSS application is not initialized.")


            project_name = f"metasurface_design_{index}"
            self.hfss_app.insert_design(project_name)

            # Generate geometry using utility function
            generate_geometry(self.hfss_app, params)
            
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
    generator.generate_designs(count=50)
