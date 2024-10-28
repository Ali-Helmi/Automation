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
    # Evaluate variables before using in HFSS commands
    cell_width = params["cell_width"]
    substrate_height = params["substrate_height"]
    patch_thickness = params["patch_thickness"]

    # Create substrate box
    hfss_app.modeler.create_box(
        position=[-float(cell_width[:-2]) / 2, -float(cell_width[:-2]) / 2, -float(substrate_height[:-2]) / 2],
        dimensions_list=[cell_width, cell_width, substrate_height],
        name="substrate",
        matname=params['material']['substrate_material']
    )

    # Create outer patches
    for i in range(1, 3):
        outer_patch_width = params[f"patch_outerWidth{i}"]
        outer_patch = hfss_app.modeler.create_rectangle(
            csPlane=hfss_app.PLANE.XY,
            position=[-float(outer_patch_width[:-2]) / 2, -float(outer_patch_width[:-2]) / 2, float(substrate_height[:-2]) / 2],
            dimension_list=[outer_patch_width, outer_patch_width],
            name=f"outer_patch{i}",
            matname=params['material']['metal_material']
        )
        hfss_app.modeler.thicken_sheet(outer_patch.name, thickness=patch_thickness)

    # Create gaps and inner patches
    for i in range(1, 3):
        gap_length = params["patch_gapLength"]
        gap_width = params["patch_gapWidth"]
        gap_position = f"-{gap_length}/2"
        patch_inner_width = params[f"patch_innerWidth{i}"]

        gap = hfss_app.modeler.create_rectangle(
            csPlane=hfss_app.PLANE.XY,
            position=[gap_position, f"{patch_inner_width}/2", float(substrate_height[:-2]) / 2],
            dimension_list=[gap_length, gap_width],
            name=f"patch_outerGap{i}",
            matname=params['material']['metal_material']
        )
        hfss_app.modeler.thicken_sheet(gap.name, thickness=patch_thickness)

        inner_patch = hfss_app.modeler.create_rectangle(
            csPlane=hfss_app.PLANE.XY,
            position=[-float(patch_inner_width[:-2]) / 2, -float(patch_inner_width[:-2]) / 2, float(substrate_height[:-2]) / 2],
            dimension_list=[patch_inner_width, patch_inner_width],
            name=f"inner_patch{i}",
            matname=params['material']['metal_material']
        )
        hfss_app.modeler.thicken_sheet(inner_patch.name, thickness=patch_thickness)

    # Create wire
    wire_width = params["wire_width"]
    wire_length = params["wire_length"]
    wire = hfss_app.modeler.create_rectangle(
        csPlane=hfss_app.PLANE.XY,
        position=[-float(wire_width[:-2]) / 2, -float(wire_length[:-2]) / 2, -float(substrate_height[:-2]) / 2 - float(patch_thickness[:-2])],
        dimension_list=[wire_width, wire_length],
        name="wire",
        matname=params['material']['metal_material']
    )
    hfss_app.modeler.thicken_sheet(wire.name, thickness=patch_thickness)

    # Create radiation box
    rad_length = params["rad_length"]
    rad_width = params["rad_width"]
    rad_height = params["rad_height"]
    hfss_app.modeler.create_box(
        position=[-float(rad_length[:-2]) / 2, -float(rad_width[:-2]) / 2, -float(rad_height[:-2]) / 2],
        dimensions_list=[rad_length, rad_width, rad_height],
        name="RadBox",
        matname=params['material']['radiation_material']
    )

    # Subtract geometry based on pattern
    hfss_app.modeler.subtract(["outer_patch1"], ["inner_patch1", "patch_outerGap1"], keep_originals=False)
    hfss_app.modeler.subtract(["outer_patch2"], ["inner_patch2", "patch_outerGap2"], keep_originals=False)


# def assign_ports_and_boundaries(hfss_app, params):
#     """
#     Assign ports and boundaries in HFSS based on design parameters.
    
#     Args:
#         hfss_app (Hfss): The HFSS application instance.
#         params (dict): Parameters including ports and boundary conditions.
#     """
#     floquet_params = params.get("boundary_conditions", {}).get("floquet_ports", [])

#     for idx, port in enumerate(floquet_params, start=1):
#         hfss_app.create_floquet_port(
#             face=port.get("face"),
#             lattice_origin=port.get("lattice_origin"),
#             lattice_b_end=port.get("lattice_b_end"),
#             lattice_a_end=port.get("lattice_a_end"),
#             nummodes=port.get("nummodes", 2),
#             portname=f"FloquetPort{idx}",
#             renorm=port.get("renorm", True),
#             deembed_dist=port.get("deembed_dist", 0),
#             reporter_filter=port.get("reporter_filter", False),
#             lattice_cs=port.get("lattice_cs", 'Global')
#         )

#     # Assign primary and secondary boundaries if available
#     primary_params = params.get("boundary_conditions", {}).get("primary", {})
#     if primary_params:
#         hfss_app.assign_primary(
#             face=primary_params.get("face"),
#             u_start=primary_params.get("u_start"),
#             u_end=primary_params.get("u_end"),
#             reverse_v=primary_params.get("reverse_v", True),
#             coord_name=primary_params.get("coord_name", 'Global'),
#             primary_name=primary_params.get("primary_name", "Primary1")
#         )

#     # Add more boundaries as needed.


def assign_ports_and_boundaries(hfss_app, params):
    # Assign Floquet ports
    hfss_app.create_floquet_port(
        face=308,
        lattice_origin=["-1.255mm", "1.255mm", "1.255mm"],
        lattice_b_end=["-1.255mm", "-1.255mm", "1.255mm"],
        lattice_a_end=["1.255mm", "1.255mm", "1.255mm"],
        nummodes=2,
        portname="FloquetPort1",
        renorm=True,
        deembed_dist=0,
        reporter_filter=False,
        lattice_cs='Global'
    )

    hfss_app.create_floquet_port(
        face=309,
        lattice_origin=["-1.255mm", "1.255mm", "-1.255mm"],
        lattice_b_end=["-1.255mm", "-1.255mm", "-1.255mm"],
        lattice_a_end=["1.255mm", "1.255mm", "-1.255mm"],
        nummodes=2,
        portname="FloquetPort2",
        renorm=True,
        deembed_dist=0,
        reporter_filter=False,
        lattice_cs='Global'
    )

    # Assign primary and secondary boundaries
    hfss_app.assign_primary(
        face=313,
        u_start=["1.255mm", "1.255mm", "-1.255mm"],
        u_end=["1.255mm", "1.255mm", "1.255mm"],
        reverse_v=True,
        coord_name='Global',
        primary_name="Primary1"
    )

    hfss_app.assign_secondary(
        face=311,
        primary_name="Primary1",
        u_start=["-1.255mm", "1.255mm", "-1.255mm"],
        u_end=["-1.255mm", "1.255mm", "1.255mm"],
        reverse_v=False,
        phase_delay='UseScanAngle',
        phase_delay_param1='0deg',
        phase_delay_param2='0deg',
        coord_name='Global',
        secondary_name="Secondary1"
    )

    hfss_app.assign_primary(
        face=312,
        u_start=["-1.255mm", "1.255mm", "-1.255mm"],
        u_end=["-1.255mm", "1.255mm", "1.255mm"],
        reverse_v=True,
        coord_name='Global',
        primary_name="Primary2"
    )

    hfss_app.assign_secondary(
        face=310,
        primary_name="Primary2",
        u_start=["-1.255mm", "-1.255mm", "-1.255mm"],
        u_end=["-1.255mm", "-1.255mm", "1.255mm"],
        reverse_v=False,
        phase_delay='UseScanAngle',
        phase_delay_param1='0deg',
        phase_delay_param2='0deg',
        coord_name='Global',
        secondary_name="Secondary2"
    )





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
