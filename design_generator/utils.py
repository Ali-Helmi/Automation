# design_generator/utils.py
# Purpose: Utility functions for geometry creation, file handling, and design manipulation

import os
from pyaedt import Hfss

def generate_geometry(hfss_app, params):
    """
    Creates geometry in HFSS based on design parameters.
    
    Args:
        hfss_app (Hfss): The HFSS application instance.
        params (dict): Parameters including dimensions, material, and pattern.
    """
    design_name = "unit_cell"
    hfss_app.modeler.create_box([0, 0, 0], 
                                [params["dimensions"]["width"], 
                                 params["dimensions"]["height"], 
                                 params["dimensions"]["thickness"]], 
                                name=design_name, material=params["material"]["metal_layer"])
    
    # Example geometry generation based on pattern type
    if params["pattern"]["type"] == "patch":
        create_patch_pattern(hfss_app, params)
    elif params["pattern"]["type"] == "slot":
        create_slot_pattern(hfss_app, params)

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
    if not os.path.exists(os.path.dirname(file_path)):
        os.makedirs(os.path.dirname(file_path))
    hfss_app.save_project(file_path)
    print(f"Project saved at {file_path}")

