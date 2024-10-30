# utils.py

import os
from pyaedt import Hfss, Desktop

def initialize_hfss_setup():
    """Set up the HFSS environment."""
    desktop = Desktop("2022.1", non_graphical=False)
    hfss_app = Hfss(projectname="Generated_Designs_Project", designname="Generated_Design", specified_version="2022.1")
    return desktop, hfss_app

def calculate_deembed_distance(params):
    """Calculate the de-embedding distance based on geometry."""
    substrate_height = float(params["substrate_height"].replace("mm", ""))
    rad_height = float(params["rad_height"].replace("mm", ""))
    deembed_distance = rad_height - (substrate_height / 2)  # Placeholder for actual calculation logic
    return f"{deembed_distance}mm"

def generate_geometry(hfss_app, params):
    """Create design geometry in HFSS."""
    hfss_app.modeler.create_box(
        position=["-cell_width/2", "-cell_width/2", "-substrate_height/2"],
        dimensions_list=["cell_width", "cell_width", "substrate_height"],
        name="substrate",
        matname=params["material"]
    )

def assign_ports(hfss_app, deembed_distance):
    """Assign ports with calculated de-embedding distance."""
    hfss_app.create_floquet_port(
        face=308,
        lattice_origin=["-1.255mm", "1.255mm", "1.255mm"],
        lattice_b_end=["-1.255mm", "-1.255mm", "1.255mm"],
        lattice_a_end=["1.255mm", "1.255mm", "1.255mm"],
        nummodes=2,
        portname="FloquetPort1",
        renorm=True,
        deembed_dist=deembed_distance,
    )

    hfss_app.create_floquet_port(
        face=309,
        lattice_origin=["-1.255mm", "1.255mm", "-1.255mm"],
        lattice_b_end=["-1.255mm", "-1.255mm", "-1.255mm"],
        lattice_a_end=["1.255mm", "1.255mm", "-1.255mm"],
        nummodes=2,
        portname="FloquetPort2",
        renorm=True,
        deembed_dist="0mm",
    )

def assign_boundaries(hfss_app):
    """Assign boundary conditions."""
    hfss_app.assign_primary(face=313, u_start=["1.255mm", "1.255mm", "-1.255mm"], u_end=["1.255mm", "1.255mm", "1.255mm"])
    hfss_app.assign_secondary(face=311, primary_name="Primary1", u_start=["-1.255mm", "1.255mm", "-1.255mm"], u_end=["-1.255mm", "1.255mm", "1.255mm"])

def save_design_file(hfss_app, file_path):
    """Save the design project to the specified file path."""
    try:
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        hfss_app.save_project(file_path)
    except OSError as e:
        print(f"Error saving file {file_path}: {e}")
