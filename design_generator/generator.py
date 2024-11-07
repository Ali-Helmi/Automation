#design_generator/generator.py
import json
import sys
import pyaedt
from design_generator.utils import setup_materials, create_geometry, assign_boundaries, create_analysis_setup, assign_ports

def main(template_path):
    with open(template_path, 'r') as file:
        params = json.load(file)

    hfss = pyaedt.Hfss(
        new_desktop_session=True,
        projectname="Generated_Designs_Project",
        designname="Generated_Design"
    )

    # Set up global variables from JSON parameters
    for key, value in params.items():
        if isinstance(value, dict):
            for sub_key, sub_value in value.items():
                if isinstance(sub_value, (int, float, str)):  # Handle only directly assignable values
                    hfss[sub_key] = sub_value
        elif isinstance(value, (int, float, str)):
            hfss[key] = value

    # Material setup
    setup_materials(hfss, params)

    # Geometry creation
    geometry_objects = create_geometry(hfss, params)

    # Port assignments
    assign_ports(hfss, geometry_objects, params)

    # Boundary assignments
    assign_boundaries(hfss, geometry_objects)

    # Analysis setup
    create_analysis_setup(hfss, params)

    # Solve
    hfss.analyze_setup("Setup1", num_cores=4)

    input("Press Enter to close the ANSYS HFSS instance...")
    hfss.release_desktop()

if __name__ == "__main__":
    if len(sys.argv) != 3 or sys.argv[1] != '--template':
        print("Usage: python generator.py --template <template_path>")
        sys.exit(1)
    template_path = sys.argv[2]
    main(template_path)
