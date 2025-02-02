# design_generator/utils.py

import random

def setup_materials(hfss, params):
    materials = params.get("materials", {})
    for name, properties in materials.items():
        if name not in hfss.materials.material_keys:
            material = hfss.materials.add_material(name)
            if "permittivity" in properties:
                material.permittivity.value = properties["permittivity"]
            if "loss_tangent" in properties:
                material.dielectric_loss_tangent.value = properties["loss_tangent"]
    if "copper" not in hfss.materials.material_keys:
        hfss.materials["copper"]

def draw_rectangle(hfss, position, dimensions, name, material):
    rectangle = hfss.modeler.create_rectangle(
        csPlane=hfss.PLANE.XY,
        position=position,
        dimension_list=dimensions,
        name=name,
        matname=material
    )
    hfss.modeler.thicken_sheet(rectangle.name, thickness="patch_thickness")
    return rectangle

def draw_circle(hfss, position, radius, name, material):
    circle = hfss.modeler.create_circle(
        cs_plane=hfss.PLANE.XY,  # Correct argument name
        position=position,
        radius=radius,
        name=name,
        matname=material
    )
    if not circle:
        raise ValueError(f"Failed to create circle: {name}")
    hfss.modeler.thicken_sheet(circle.name, thickness="patch_thickness")
    return circle

def create_geometry(hfss, params):
    geometry_params = params.get("geometry", {})
    shapes = params.get("shapes", [])
    operations = params.get("operations", [])
    created_objects = {}

    substrate_material = geometry_params.get("substrate_material", "FR4_epoxy")
    radiation_material = geometry_params.get("radiation_material", "vacuum")

    for key, value in geometry_params.items():
        if isinstance(value, str):
            hfss[key] = value

    substrate = hfss.modeler.create_box(
        position=["-cell_width/2", "-cell_width/2", "-substrate_height/2"],
        dimensions_list=["cell_width", "cell_width", "substrate_height"],
        name="substrate",
        matname=substrate_material
    )

    created_objects["substrate"] = substrate

    for shape in shapes:
        shape_type = shape["type"]
        dimensions = shape["dimensions"]
        material = shape.get("material", "copper")  # Ensure the material is copper
        name = shape.get("name", shape_type)

        if shape_type == "rectangle":
            obj = draw_rectangle(hfss, dimensions["position"], dimensions["size"], name, material)
        elif shape_type == "circle":
            obj = draw_circle(hfss, dimensions["position"], dimensions["radius"], name, material)
        else:
            raise ValueError(f"Unsupported shape type: {shape_type}")

        created_objects[name] = obj

    rad_box = hfss.modeler.create_box(
        position=["-rad_length/2", "-rad_width/2", "-rad_height/2"],
        dimensions_list=["rad_length", "rad_width", "rad_height"],
        name="RadBox",
        matname=radiation_material
    )

    created_objects["rad_box"] = rad_box

    for operation in operations:
        op_type = operation["type"]
        new_name = operation["new_name"]

        if op_type == "merge":
            objects = operation["objects"]
            merged_object = merge_objects(hfss, objects, new_name)
            created_objects[new_name] = merged_object
        elif op_type == "subtract":
            blank_name = operation["blank"]
            tool_name = operation["tool"]
            subtracted_object = subtract_objects(hfss, blank_name, tool_name, new_name)
            created_objects[new_name] = subtracted_object
        else:
            raise ValueError(f"Unsupported operation type: {op_type}")

    return created_objects

def create_patch(hfss, params):
    geometry_params = params.get("geometry", {})
    
    # Get material names as strings
    substrate_material = geometry_params.get("substrate_material", "FR4_epoxy")
    radiation_material = geometry_params.get("radiation_material", "vacuum")
    
    # Set variables first
    for key, value in geometry_params.items():
        if isinstance(value, str):  # Only set string values
            hfss[key] = value

    substrate = hfss.modeler.create_box(
        position=["-cell_width/2", "-cell_width/2", "-substrate_height/2"], 
        dimensions_list=["cell_width", "cell_width", "substrate_height"],
        name="substrate", 
        matname=substrate_material
    )

    metal_patch = hfss.modeler.create_rectangle(
        csPlane=hfss.PLANE.XY,
        position=["-cell_width/2", "-cell_width/2", "substrate_height/2"],
        dimension_list=["cell_width", "cell_width"],
        name="metal_patch",
        matname="copper"
    )
    hfss.modeler.thicken_sheet(metal_patch.name, thickness="patch_thickness")
    
    rad_box = hfss.modeler.create_box(
        position=["-rad_length/2", "-rad_width/2", "-rad_height/2"], 
        dimensions_list=["rad_length", "rad_width", "rad_height"],
        name="RadBox", 
        matname=radiation_material
    )
    
    return {
        "substrate": substrate,
        "metal_patch": metal_patch,
        "rad_box": rad_box
    }

def assign_ports(hfss, geometry_objects, params):
    box = geometry_objects["rad_box"]
    geometry_params = params.get("geometry", {})

    for key, value in geometry_params.items():
        if isinstance(value, str):  # Only set string values
            hfss[key] = value
    
    floquet_port1 = hfss.create_floquet_port(
        face=[face for face in box.faces if face.normal == [0, 0, 1]][0].id, 
        lattice_origin=[face for face in box.faces if face.normal == [0, 0, 1]][0].vertices[2].position, 
        lattice_b_end=[face for face in box.faces if face.normal == [0, 0, 1]][0].vertices[3].position, 
        lattice_a_end=[face for face in box.faces if face.normal == [0, 0, 1]][0].vertices[1].position, 
        nummodes=2, 
        portname="FloquetPort1", 
        renorm=True, 
        deembed_dist="(rad_height/2) - (substrate_height/2) - patch_thickness", 
        reporter_filter=False, 
        lattice_cs='Global'
    )

    floquet_port2 = hfss.create_floquet_port(
        face=[face for face in box.faces if face.normal == [0, 0, -1]][0].id, 
        lattice_origin=[face for face in box.faces if face.normal == [0, 0, -1]][0].vertices[3].position, 
        lattice_b_end=[face for face in box.faces if face.normal == [0, 0, -1]][0].vertices[2].position, 
        lattice_a_end=[face for face in box.faces if face.normal == [0, 0, -1]][0].vertices[0].position, 
        nummodes=2, 
        portname="FloquetPort2", 
        renorm=True, 
        deembed_dist=0, 
        reporter_filter=False, 
        lattice_cs='Global'
    )

def assign_boundaries(hfss, geometry_objects):
    box = geometry_objects["rad_box"]
    
    primary1 = hfss.assign_primary(
        face=[face for face in box.faces if face.normal == [1, 0, 0]][0].id, 
        u_start=[face for face in box.faces if face.normal == [1, 0, 0]][0].vertices[2].position, 
        u_end=[face for face in box.faces if face.normal == [1, 0, 0]][0].vertices[3].position, 
        reverse_v=True, 
        coord_name='Global', 
        primary_name="Primary1"
    )

    secondary1 = hfss.assign_secondary(
        face=[face for face in box.faces if face.normal == [-1, 0, 0]][0].id, 
        primary_name="Primary1", 
        u_start=[face for face in box.faces if face.normal == [-1, 0, 0]][0].vertices[1].position, 
        u_end=[face for face in box.faces if face.normal == [-1, 0, 0]][0].vertices[0].position, 
        reverse_v=False, 
        phase_delay='UseScanAngle', 
        phase_delay_param1='0deg', 
        phase_delay_param2='0deg', 
        coord_name='Global', 
        secondary_name="Secondary1"
    )

    primary2 = hfss.assign_primary(
        face=[face for face in box.faces if face.normal == [0, 1, 0]][0].id, 
        u_start=[face for face in box.faces if face.normal == [0, 1, 0]][0].vertices[2].position, 
        u_end=[face for face in box.faces if face.normal == [0, 1, 0]][0].vertices[3].position, 
        reverse_v=True, 
        coord_name='Global', 
        primary_name="Primary2"
    )

    secondary2 = hfss.assign_secondary(
        face=[face for face in box.faces if face.normal == [0, -1, 0]][0].id, 
        primary_name="Primary2", 
        u_start=[face for face in box.faces if face.normal == [0, -1, 0]][0].vertices[1].position, 
        u_end=[face for face in box.faces if face.normal == [0, -1, 0]][0].vertices[0].position, 
        reverse_v=False, 
        phase_delay='UseScanAngle', 
        phase_delay_param1='0deg', 
        phase_delay_param2='0deg', 
        coord_name='Global', 
        secondary_name="Secondary2"
    )

def create_analysis_setup(hfss, params):
    analysis_params = params.get("analysis", {})
    
    # Set frequency variables first
    hfss["lower_frequency"] = analysis_params["frequency_start"]
    hfss["upper_frequency"] = analysis_params["frequency_stop"]
    hfss["solution_frequency"] = analysis_params["solution_frequency"]

    setup = hfss.create_setup("Setup1")
    setup.props["Frequency"] = hfss["solution_frequency"]
    setup["MaximumPasses"] = 21
    
    # Extract numeric values from frequency strings
    freq_start = float(analysis_params["frequency_start"].replace("GHz", ""))
    freq_stop = float(analysis_params["frequency_stop"].replace("GHz", ""))
    
    hfss.create_linear_count_sweep(
        setupname="Setup1",
        unit="GHz",
        freqstart=freq_start,
        freqstop=freq_stop,
        num_of_freq_points=501,
        sweepname="sweep1",
        sweep_type="Interpolating",
        save_fields=False
    )

def merge_objects(hfss, object_names, new_name):
    """Merge multiple objects into a single object."""
    success = hfss.modeler.unite(object_names)
    if not success:
        raise ValueError(f"Failed to merge objects: {object_names}")
    merged_object = hfss.modeler.get_object_from_name(object_names[0])
    merged_object.name = new_name
    return merged_object

def subtract_objects(hfss, blank_name, tool_name, new_name):
    """Subtract a tool object from a blank object."""
    success = hfss.modeler.subtract([blank_name], [tool_name])
    if not success:
        raise ValueError(f"Failed to subtract object: {tool_name} from {blank_name}")
    subtracted_object = hfss.modeler.get_object_from_name(blank_name)
    subtracted_object.name = new_name
    return subtracted_object
