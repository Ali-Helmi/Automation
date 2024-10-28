# design_generator/utils.py
# Purpose: Utility functions for geometry creation, file handling, and design manipulation

import os
from pyaedt import Hfss

def generate_geometry(hfss_app, params):
    # Create substrate
    substrate = hfss_app.modeler.create_box(
        position=["-params['dimensions']['width']/2", "-params['dimensions']['height']/2", "-params['dimensions']['thickness']/2"], 
        dimensions_list=["params['dimensions']['width']", "params['dimensions']['height']", "params['dimensions']['thickness']"],
        name="substrate", 
        matname=params["material"]["substrate"]["type"]
    )

    # Create patches and subtract gaps
    outer_patch1 = hfss_app.modeler.create_rectangle(
        csPlane=hfss_app.PLANE.XY,
        position=["-params['dimensions']['width']/2", "-params['dimensions']['width']/2", "params['dimensions']['thickness']/2"],
        dimension_list=["params['dimensions']['width'] * 0.8", "params['dimensions']['width'] * 0.8"],
        name="outer_patch1",
        matname=params["material"]["metal_layer"]
    )
    hfss_app.modeler.thicken_sheet(outer_patch1.name, thickness="params['dimensions']['thickness']")
    
    # Add the rest of the patches and gaps similarly
    # Perform subtraction operations for gap creation
    hfss_app.modeler.subtract(["outer_patch1"], ["gap_patch"], keep_originals=False)

    # Add Floquet port assignments and primary/secondary assignments as in the example
    hfss_app.create_floquet_port(
        face=308,
        lattice_origin=["0", "0", "0"],
        lattice_b_end=["0", "-params['dimensions']['width']", "0"],
        lattice_a_end=["params['dimensions']['width']", "0", "0"],
        nummodes=2,
        portname="FloquetPort1",
        renorm=True,
        deembed_dist=0
    )
    # Similarly, add other ports and boundary conditions


def create_patch_pattern(hfss_app, params):
    """
    Generates a patch pattern on the design.
    
    Args:
        hfss_app (Hfss): The HFSS application instance.
        params (dict): Parameters including pattern details.
    """
    width = params["dimensions"]["width"] * 0.8
    height = params["dimensions"]["height"] * 0.8
    hfss_app.modeler.create_rectangle([0, 0, params["dimensions"]["thickness"]], 
                                      [width, height], 
                                      name="patch", material=params["material"]["metal_layer"])

def create_slot_pattern(hfss_app, params):
    """
    Generates a slot pattern on the design.
    
    Args:
        hfss_app (Hfss): The HFSS application instance.
        params (dict): Parameters including pattern details.
    """
    slot_width = params["dimensions"]["width"] * 0.4
    slot_height = params["dimensions"]["height"] * 0.4
    hfss_app.modeler.create_rectangle([params["dimensions"]["width"]/2 - slot_width/2, 
                                       params["dimensions"]["height"]/2 - slot_height/2, 
                                       params["dimensions"]["thickness"]],
                                      [slot_width, slot_height], 
                                      name="slot", material="vacuum")

def save_design_file(hfss_app, file_path):
    """
    Saves the HFSS design file.
    
    Args:
        hfss_app (Hfss): The HFSS application instance.
        file_path (str): Path to save the file.
    """
    try:
        if not os.path.exists(os.path.dirname(file_path)):
            os.makedirs(os.path.dirname(file_path))
        hfss_app.save_project(file_path)
        print(f"Project saved at {file_path}")
    except OSError as e:
        print(f"Error saving file {file_path}: {e}")
