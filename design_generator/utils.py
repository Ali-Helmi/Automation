# design_generator/utils.py
import json
import os
from pyaedt import Hfss

def load_template(template_path):
    try:
        with open(template_path, 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        print(f"Error: Template file {template_path} not found.")
        return {}

def generate_geometry(hfss_app, params):
    # Create substrate and patches with exact positions and dimensions
    hfss_app.modeler.create_box(
        position=["-cell_width/2", "-cell_width/2", "-substrate_height/2"],
        dimensions_list=["cell_width", "cell_width", "substrate_height"],
        name="substrate",
        matname=params["substrate_material"]
    )

    outer_patch1 = hfss_app.modeler.create_rectangle(
        csPlane=hfss_app.PLANE.XY,
        position=["-patch_outerWidth1/2", "-patch_outerWidth1/2", "substrate_height/2"],
        dimension_list=["patch_outerWidth1", "patch_outerWidth1"],
        name="outer_patch1",
        matname="copper"
    )
    hfss_app.modeler.thicken_sheet(outer_patch1.name, thickness="patch_thickness")

    outer_patch2 = hfss_app.modeler.create_rectangle(
        csPlane=hfss_app.PLANE.XY,
        position=["-patch_outerWidth2/2", "-patch_outerWidth2/2", "substrate_height/2"],
        dimension_list=["patch_outerWidth2", "patch_outerWidth2"],
        name="outer_patch2",
        matname="copper"
    )
    hfss_app.modeler.thicken_sheet(outer_patch2.name, thickness="patch_thickness")

    # Add inner patches, gaps, and other elements in exact configurations

def initialize_parameters_and_setup(hfss_app, params):
    # Assign parameters from the template directly
    hfss_app["cell_width"] = params["cell_width"]
    hfss_app["patch_outerWidth1"] = params["patch_outerWidth1"]
    hfss_app["patch_outerWidth2"] = params["patch_outerWidth2"]
    hfss_app["patch_innerWidth1"] = params["patch_innerWidth1"]
    hfss_app["patch_innerWidth2"] = params["patch_innerWidth2"]
    hfss_app["patch_gapLength"] = params["patch_gapLength"]
    hfss_app["patch_gapWidth"] = params["patch_gapWidth"]
    hfss_app["substrate_height"] = params["substrate_height"]
    hfss_app["wire_length"] = params["wire_length"]
    hfss_app["wire_width"] = params["wire_width"]
    hfss_app["rad_length"] = params["rad_length"]
    hfss_app["rad_width"] = params["rad_width"]
    hfss_app["rad_height"] = params["rad_height"]

    # Set up HFSS solution parameters
    setup = hfss_app.create_setup("Setup1")
    setup.props["Frequency"] = params["solution_frequency"]
    setup["MaximumPasses"] = 21
    hfss_app.create_linear_count_sweep(
        setupname="Setup1", unit="GHz", freqstart=5, freqstop=15,
        num_of_freq_points=501, sweepname="sweep1", sweep_type="Interpolating", save_fields=False
    )

def calculate_deembed_distance(params):
    """Calculate and return the deembedding distance based on geometry."""
    substrate_height = float(params["substrate_height"].replace("mm", ""))
    rad_height = float(params["rad_height"].replace("mm", ""))
    return f"{rad_height - (substrate_height / 2)}mm"

def assign_ports_and_boundaries(hfss_app, deembed_distance):
    hfss_app.create_floquet_port(
        face=308,
        lattice_origin=["-1.255mm", "1.255mm", "1.255mm"],
        lattice_b_end=["-1.255mm", "-1.255mm", "1.255mm"],
        lattice_a_end=["1.255mm", "1.255mm", "1.255mm"],
        nummodes=2,
        portname="FloquetPort1",
        renorm=True,
        deembed_dist=deembed_distance
    )

    hfss_app.create_floquet_port(
        face=309,
        lattice_origin=["-1.255mm", "1.255mm", "-1.255mm"],
        lattice_b_end=["-1.255mm", "-1.255mm", "-1.255mm"],
        lattice_a_end=["1.255mm", "1.255mm", "-1.255mm"],
        nummodes=2,
        portname="FloquetPort2",
        renorm=True,
        deembed_dist="0mm"
    )

def save_design_file(hfss_app, output_dir):
    file_path = os.path.join(output_dir, "Generated_Design.aedt")
    hfss_app.save_project(file_path)
    print(f"Project saved at {file_path}")
