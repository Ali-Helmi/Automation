# design_generator/generator.py

import json
import sys
import pyaedt
from design_generator.utils import setup_materials, create_geometry, assign_boundaries, create_analysis_setup, assign_ports
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")
pyaedt_logger = logging.getLogger('pyaedt')
pyaedt_logger.setLevel(logging.INFO)  # Set pyaedt logging level to INFO

# Mute specific debug messages
export_logger = logging.getLogger('pyaedt.modeler.Primitives3D')
export_logger.setLevel(logging.WARNING)  # Set to WARNING to mute debug messages

def main(template_paths):

    hfss = pyaedt.Hfss(
        new_desktop_session=True,
        projectname="Generated_Designs_Project"
    )

    for index, template_path in enumerate(template_paths):
        with open(template_path, 'r') as file:
            params = json.load(file)

        hfss.insert_design(f"Design_{index + 1}", "DrivenModal")

        setup_materials(hfss, params)
        geometry_objects = create_geometry(hfss, params)
        assign_ports(hfss, geometry_objects, params)
        assign_boundaries(hfss, geometry_objects)
        create_analysis_setup(hfss, params)

        print(f"Design {index + 1} created.")

    input("Press Enter to close the ANSYS HFSS instance...")
    hfss.release_desktop()

if __name__ == "__main__":
    if len(sys.argv) < 3 or sys.argv[1] != '--templates':
        print("Usage: python generator.py --templates <template1_path> <template2_path> ...")
        sys.exit(1)
    template_paths = sys.argv[2:]
    main(template_paths)
