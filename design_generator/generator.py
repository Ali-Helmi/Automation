import json
import pyaedt
from utils import load_template, setup_logger

# Initialize logger
logger = setup_logger()

# Load design parameters from JSON template
params = load_template("design_generator/templates/template_1.json")
if not params:
    logger.error("Failed to load design parameters.")
    exit(1)

# Initialize HFSS with new session
hfss = pyaedt.Hfss(
    new_desktop_session=True,
    projectname="Generated_Designs_Project",
    designname="Generated_Design"
)

# Assign material properties
hfss["substrate_material"] = params["substrate_material"]
hfss["radiation_material"] = params["radiation_material"]
hfss.materials["copper"]

# Assign dimensions
for key, value in params.items():
    hfss[key] = value

# Geometry Creation
try:
    substrate = hfss.modeler.create_box(
        position=["-cell_width/2", "-cell_width/2", "-substrate_height/2"],
        dimensions_list=["cell_width", "cell_width", "substrate_height"],
        name="substrate",
        matname=params["substrate_material"]
    )

    # Patch and Gap layers
    outer_patch1 = hfss.modeler.create_rectangle(
        csPlane=hfss.PLANE.XY,
        position=["-patch_outerWidth1/2", "-patch_outerWidth1/2", "substrate_height/2"],
        dimension_list=["patch_outerWidth1", "patch_outerWidth1"],
        name="outer_patch1",
        matname="copper"
    )
    hfss.modeler.thicken_sheet(outer_patch1.name, thickness="patch_thickness")

    outer_patch2 = hfss.modeler.create_rectangle(
        csPlane=hfss.PLANE.XY,
        position=["-patch_outerWidth2/2", "-patch_outerWidth2/2", "substrate_height/2"],
        dimension_list=["patch_outerWidth2", "patch_outerWidth2"],
        name="outer_patch2",
        matname="copper"
    )
    hfss.modeler.thicken_sheet(outer_patch2.name, thickness="patch_thickness")

    # Gaps and Inner patches
    patch_outerGap = hfss.modeler.create_rectangle(
        csPlane=hfss.PLANE.XY,
        position=["-patch_gapLength/2", "-patch_outerWidth1/2", "substrate_height/2"],
        dimension_list=["patch_gapLength", "patch_gapWidth"],
        name="patch_outerGap",
        matname="copper"
    )
    hfss.modeler.thicken_sheet(patch_outerGap.name, thickness="patch_thickness")

    inner_patch1 = hfss.modeler.create_rectangle(
        csPlane=hfss.PLANE.XY,
        position=["-patch_innerWidth1/2", "-patch_innerWidth1/2", "substrate_height/2"],
        dimension_list=["patch_innerWidth1", "patch_innerWidth1"],
        name="inner_patch1",
        matname="copper"
    )
    hfss.modeler.thicken_sheet(inner_patch1.name, thickness="patch_thickness")

    wire = hfss.modeler.create_rectangle(
        csPlane=hfss.PLANE.XY,
        position=["-wire_width/2", "-wire_length/2", "-substrate_height/2 -patch_thickness"],
        dimension_list=["wire_width", "wire_length"],
        name="wire",
        matname="copper"
    )
    hfss.modeler.thicken_sheet(wire.name, thickness="patch_thickness")

    rad_box = hfss.modeler.create_box(
        position=["-rad_length/2", "-rad_width/2", "-rad_height/2"],
        dimensions_list=["rad_length", "rad_width", "rad_height"],
        name="RadBox",
        matname=params["radiation_material"]
    )

    # Subtraction for precise design
    hfss.modeler.subtract(["outer_patch1"], ["inner_patch1", "patch_outerGap"], keep_originals=False)
    hfss.modeler.subtract(["outer_patch2"], ["inner_patch2"], keep_originals=False)

    logger.info("Geometry created successfully.")

except Exception as e:
    logger.error(f"Error creating geometry: {str(e)}")

# Floquet Port and Boundary Conditions
try:
    floquet_port1 = hfss.create_floquet_port(
        face=308,
        lattice_origin=["-1.255mm", "1.255mm", "1.255mm"],
        lattice_b_end=["-1.255mm", "-1.255mm", "1.255mm"],
        lattice_a_end=["1.255mm", "1.255mm", "1.255mm"],
        nummodes=2,
        portname="FloquetPort1"
    )
    floquet_port2 = hfss.create_floquet_port(
        face=309,
        lattice_origin=["-1.255mm", "1.255mm", "-1.255mm"],
        lattice_b_end=["-1.255mm", "-1.255mm", "-1.255mm"],
        lattice_a_end=["1.255mm", "1.255mm", "-1.255mm"],
        nummodes=2,
        portname="FloquetPort2"
    )
    logger.info("Floquet ports assigned successfully.")
except Exception as e:
    logger.error(f"Error assigning ports: {str(e)}")

# Simulation Setup
try:
    setup = hfss.create_setup("Setup1")
    setup.props["Frequency"] = params["solution_frequency"]
    setup["MaximumPasses"] = 21
    hfss.create_linear_count_sweep(
        setupname="Setup1",
        unit="GHz",
        freqstart=params["lower_frequency"],
        freqstop=params["upper_frequency"],
        num_of_freq_points=501,
        sweepname="sweep1",
        sweep_type="Interpolating",
        save_fields=False
    )
    hfss.analyze_setup("Setup1")
    logger.info("Simulation setup and analysis completed.")
except Exception as e:
    logger.error(f"Error in simulation setup: {str(e)}")

input("Press Enter to close the ANSYS HFSS instance...")
hfss.release_desktop()
