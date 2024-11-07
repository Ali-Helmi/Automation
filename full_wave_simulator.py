#full_wave_simulator.py
import pyaedt
hfss = pyaedt.Hfss(
    new_desktop_session=True,
    projectname="Scripting",
    designname="full_wave_simulator")

# hfss.set_units('Length', 'mm')


substrate_material = "FR4_epoxy"
radiation_material = "vacuum"
dielectric_constant = 4.4
loss_tangent = 0.001


hfss["cell_width"] = "2.5mm"
hfss["patch_outerWidth1"] = "2.2mm"
hfss["patch_outerWidth2"] = "1.5mm"
hfss["patch_innerWidth1"] = "1.8mm"
hfss["patch_innerWidth2"] = "1.1mm"
hfss["patch_gapLength"] = "0.3mm"
hfss["patch_gapWidth"] = "0.2mm"
hfss["substrate_height"] = "0.25mm"
hfss["wire_length"] = "2.5mm"
hfss["wire_width"] = "0.14mm"
hfss["rad_length"] = "2.51mm"
hfss["rad_width"] = "2.51mm"
hfss["rad_height"] = "2.51mm"

hfss["lower_frequency"] = "5GHz"
hfss["upper_frequency"] = "15GHz"
hfss["solution_frequency"] = "10GHz"
hfss["patch_thickness"] = "0.017mm"
hfss["wavelength"] = "29.97925mm"



metal = hfss.materials["copper"]


substrate = hfss.modeler.create_box(position=["-cell_width/2","-cell_width/2","-substrate_height/2"], 
                                  dimensions_list=["cell_width", "cell_width", "substrate_height"],
                                  name="substrate", 
                                  matname=substrate_material)

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

patch_outerGap = hfss.modeler.create_rectangle(
    csPlane=hfss.PLANE.XY,
    position=["-patch_gapLength/2", "-patch_outerWidth1/2", "substrate_height/2"],
    dimension_list=["patch_gapLength", "patch_gapWidth"],
    name="patch_outerGap",
    matname="copper"
)
hfss.modeler.thicken_sheet(patch_outerGap.name, thickness="patch_thickness")

patch_innerGap = hfss.modeler.create_rectangle(
    csPlane=hfss.PLANE.XY,
    position=["-patch_gapLength/2", "patch_innerWidth2/2", "substrate_height/2"],
    dimension_list=["patch_gapLength", "patch_gapWidth"],
    name="patch_innerGap",
    matname="copper"
)
hfss.modeler.thicken_sheet(patch_innerGap.name, thickness="patch_thickness")

inner_patch1 = hfss.modeler.create_rectangle(
    csPlane=hfss.PLANE.XY,
    position=["-patch_innerWidth1/2", "-patch_innerWidth1/2", "substrate_height/2"],
    dimension_list=["patch_innerWidth1", "patch_innerWidth1"],
    name="inner_patch1",
    matname="copper"
)
hfss.modeler.thicken_sheet(inner_patch1.name, thickness="patch_thickness")

inner_patch2 = hfss.modeler.create_rectangle(
    csPlane=hfss.PLANE.XY,
    position=["-patch_innerWidth2/2", "-patch_innerWidth2/2", "substrate_height/2"],
    dimension_list=["patch_innerWidth2", "patch_innerWidth2"],
    name="inner_patch2",
    matname="copper"
)
hfss.modeler.thicken_sheet(inner_patch2.name, thickness="patch_thickness")

wire = hfss.modeler.create_rectangle(
    csPlane=hfss.PLANE.XY,
    position=["-wire_width/2", "-wire_length/2", "-substrate_height/2 -patch_thickness"],
    dimension_list=["wire_width", "wire_length"],
    name="wire",
    matname="copper"
)
hfss.modeler.thicken_sheet(wire.name, thickness="patch_thickness")

rad_box = hfss.modeler.create_box(position=["-rad_length/2","-rad_width/2","-rad_height/2"], 
                                  dimensions_list=["rad_length", "rad_width", "rad_height"],
                                  name="RadBox", 
                                  matname=radiation_material)


hfss.modeler.subtract(["outer_patch1"], ["inner_patch1", "patch_outerGap"], keep_originals=False)
hfss.modeler.subtract(["outer_patch2"], ["inner_patch2", "patch_innerGap"], keep_originals=False)

box = rad_box

#[face for face in box.faces if face.normal == [0, 0, 1]][0].vertices[0].position

floquet_port1 = hfss.create_floquet_port(face=[face for face in box.faces if face.normal == [0, 0, 1]][0].id, 
                         lattice_origin=[face for face in box.faces if face.normal == [0, 0, 1]][0].vertices[2].position, 
                         lattice_b_end=[face for face in box.faces if face.normal == [0, 0, 1]][0].vertices[3].position, 
                         lattice_a_end=[face for face in box.faces if face.normal == [0, 0, 1]][0].vertices[1].position, 
                         nummodes=2, 
                         portname="FloquetPort1", 
                         renorm=True, 
                         deembed_dist="1.113mm", 
                         reporter_filter=False, 
                         lattice_cs='Global')

floquet_port2 = hfss.create_floquet_port(face=[face for face in box.faces if face.normal == [0, 0, -1]][0].id, 
                         lattice_origin=[face for face in box.faces if face.normal == [0, 0, -1]][0].vertices[3].position, 
                         lattice_b_end=[face for face in box.faces if face.normal == [0, 0, -1]][0].vertices[2].position, 
                         lattice_a_end=[face for face in box.faces if face.normal == [0, 0, -1]][0].vertices[0].position, 
                         nummodes=2, 
                         portname="FloquetPort2", 
                         renorm=True, 
                         deembed_dist=0, 
                         reporter_filter=False, 
                         lattice_cs='Global')

primary1 = hfss.assign_primary(face=[face for face in box.faces if face.normal == [1, 0, 0]][0].id, 
                              u_start=[face for face in box.faces if face.normal == [1, 0, 0]][0].vertices[2].position, 
                              u_end=[face for face in box.faces if face.normal == [1, 0, 0]][0].vertices[3].position, 
                              reverse_v=True, 
                              coord_name='Global', 
                              primary_name="Primary1")

secondary1 = hfss.assign_secondary(face=[face for face in box.faces if face.normal == [-1, 0, 0]][0].id, 
                                  primary_name="Primary1", 
                                  u_start=[face for face in box.faces if face.normal == [-1, 0, 0]][0].vertices[1].position, 
                                  u_end=[face for face in box.faces if face.normal == [-1, 0, 0]][0].vertices[0].position, 
                                  reverse_v=False, 
                                  phase_delay='UseScanAngle', 
                                  phase_delay_param1='0deg', 
                                  phase_delay_param2='0deg', 
                                  coord_name='Global', 
                                  secondary_name="Secondary1")

primary2 = hfss.assign_primary(face=[face for face in box.faces if face.normal == [0, 1, 0]][0].id, 
                              u_start=[face for face in box.faces if face.normal == [0, 1, 0]][0].vertices[2].position, 
                              u_end=[face for face in box.faces if face.normal == [0, 1, 0]][0].vertices[3].position, 
                              reverse_v=True, 
                              coord_name='Global', 
                              primary_name="Primary2")

secondary2 = hfss.assign_secondary(face=[face for face in box.faces if face.normal == [0, -1, 0]][0].id, 
                                  primary_name="Primary2", 
                                  u_start=[face for face in box.faces if face.normal == [0, -1, 0]][0].vertices[1].position, 
                                  u_end=[face for face in box.faces if face.normal == [0, -1, 0]][0].vertices[0].position, 
                                  reverse_v=False, 
                                  phase_delay='UseScanAngle', 
                                  phase_delay_param1='0deg', 
                                  phase_delay_param2='0deg', 
                                  coord_name='Global', 
                                  secondary_name="Secondary2")


# setup = hfss.create_setup(setupname="Setup1", setuptype="HFSSDrivenAuto", unit = "GHz", freqstart = 7, freqstop = 14, sweep_type="Interpolating", save_fields=False)
setup = hfss.create_setup("Setup1")
setup.props["Frequency"] = "solution_frequency"
setup["MaximumPasses"] = 21
hfss.create_linear_count_sweep(setupname="Setup1", unit="GHz", freqstart=5, freqstop=15,
num_of_freq_points=501, sweepname="sweep1",
sweep_type="Interpolating", save_fields=False)

# SetupHFSSAuto.analyze(num_cores=1, num_tasks=1, num_gpu=0, acf_file=None, use_auto_settings=True, solve_in_batch=False, machine='localhost', run_in_thread=False, revert_to_initial_mesh=False, blocking=True)
hfss.analyze_setup("Setup1", num_cores=4, num_tasks=1, num_gpu=0, acf_file=None, use_auto_settings=True, num_variations_to_distribute=None, allowed_distribution_types=None, revert_to_initial_mesh=False, blocking=True)


input("Press Enter to close the ANSYS HFSS instance...")
hfss.release_desktop()
