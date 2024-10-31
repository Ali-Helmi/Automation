# generator.py
import argparse
import logging
from pyaedt import Hfss, Desktop
from design_generator.utils import (
    load_template, generate_geometry, initialize_parameters_and_setup,
    assign_ports_and_boundaries, calculate_deembed_distance, save_design_file
)

class DesignGenerator:
    def __init__(self, template_path, output_dir="./designs"):
        logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
        self.template_path = template_path
        self.output_dir = output_dir
        self.designs = []
        self.desktop = None
        self.hfss_app = None

    def initialize_hfss(self):
        """Initialize the HFSS application and set up a new project."""
        logging.info("Initializing HFSS...")
        self.desktop = Desktop("2022.1", non_graphical=False)
        self.hfss_app = Hfss(
            projectname="Generated_Designs_Project",
            designname="Generated_Design",
            specified_version="2022.1",
            new_desktop_session=False
        )
        logging.info("HFSS initialized successfully.")

    def load_design_template(self):
        template = load_template(self.template_path)
        if template is None:
            raise FileNotFoundError(f"Template file {self.template_path} could not be loaded.")
        logging.info(f"Loaded design parameters: {template}")
        return template

    def create_and_save_design(self, design_params):
        try:
            logging.info("Generating geometry...")
            generate_geometry(self.hfss_app, design_params)
            logging.info("Setting parameters and creating setup...")
            initialize_parameters_and_setup(self.hfss_app, design_params)
            logging.info("Calculating deembed distance...")
            deembed_distance = calculate_deembed_distance(design_params)
            logging.info("Assigning ports and boundaries...")
            assign_ports_and_boundaries(self.hfss_app, deembed_distance)
            logging.info("Saving the design project...")
            save_design_file(self.hfss_app, self.output_dir)
            logging.info("Design saved successfully.")
        except Exception as e:
            logging.error(f"An error occurred during design creation: {e}")

    def cleanup_hfss(self):
        """Prevent HFSS from closing immediately; waits for manual input."""
        input("Press Enter to close the ANSYS HFSS instance...")
        if self.hfss_app:
            logging.info("Closing HFSS project.")
            self.hfss_app.close_project()
        if self.desktop:
            logging.info("Closing AEDT Desktop session.")
            self.desktop.close_desktop()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate HFSS designs with specified template.")
    parser.add_argument("--template", type=str, default="templates/template_1.json",
                        help="Path to the JSON template file for design parameters.")
    args = parser.parse_args()

    generator = DesignGenerator(template_path=args.template)
    generator.initialize_hfss()
    design_params = generator.load_design_template()
    generator.create_and_save_design(design_params)
    generator.cleanup_hfss()
