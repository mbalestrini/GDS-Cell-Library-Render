import bpy
from bpy.types import LayerCollection, Material
import sys # read command-line arguments
import os
import json 


D = bpy.data
C = bpy.context

# SETTINGS
SCALE = 1.0
SKIP_UNNAMED_LAYERS = True
EXCLUDE_LAYER_IDS = [] #["67/5"]
RESOLUTION_PERCENTAGE = 50



import argparse


print(sys.argv)

# If the script was executed from the command line we read the parameters after the "--" 
if("--" in sys.argv):
    script_argv = sys.argv[sys.argv.index("--") + 1 : ].copy()
else:
    script_argv = sys.argv.copy()

argparser = argparse.ArgumentParser()
argparser.add_argument('-i', "--input_json", required=False, help="Input GDS json file")
argparser.add_argument('-o', "--output_path", required=False, help="Path to put the generated render files")
argparser.add_argument('-s', "--scale", required=False, type=float,  help="Scaling multiplier of input geometry")
#args = vars(argparser.parse_args(script_argv))
args = vars(argparser.parse_known_args(script_argv)[0])
    


# input_cell_json_path might be defined inside blender when running the script from the IDE
global input_cell_json_path
try: 
    input_cell_json_path
except NameError: 
    input_cell_json_path = None
if(input_cell_json_path==None):
    if(args["input_json"]!=None):
        # last arguments is the cell json file
        input_cell_json_path = args["input_json"]
    else:
        print("hardcoded import file for testing")
        input_cell_json_path = "Y:/home/videogamo/Work/GDS_and_Blender/gds/sky130_fd_sc_hd/json/sky130_fd_sc_hd__mux2_1.json"


# output directory
output_path = ""    
if(args["output_path"]!=None):
    output_path = args["output_path"]
    try:
        os.makedirs(output_path, exist_ok = True)
    except OSError as error:
        print("Output directory '%s' can not be created" % output_path)
        exit()


if(args["scale"]):
    SCALE = args["scale"]




cell_file = open(input_cell_json_path, "r")
cell = json.load(cell_file)
cell_file.close()

# to store objects created for faster manipulation
layer_objects = {}


print("Cell Layers:")
for layer_id, layer in cell["layers"].items():
    print(layer_id, layer["name"], "polygons", len(layer["polygons"]))


# Create "CELL" collection and link it
cell_collection = D.collections.new("CELL")
C.scene.collection.children.link(cell_collection)
# Select "CELL" as active collection
collections = bpy.context.view_layer.layer_collection.children
for collection in collections:
    if collection.name == "CELL":
        bpy.context.view_layer.active_layer_collection = collection




for layer_id, layer in cell["layers"].items():
    if(SKIP_UNNAMED_LAYERS and layer["name"]==""):
        print("Skipping unnamed layer:", layer_id)
        continue
    if(layer_id in EXCLUDE_LAYER_IDS):
        print("Skipping excluded layer:", layer_id)
        continue

    print("Importing layer",  layer_id, layer["name"])

    material_name = layer_id

    layer_objects[layer_id] = []

    
    obj_name = layer_id + "_" + layer["name"]

    layer_objectdata = D.objects.new( obj_name, None )
    layer_objectdata.empty_display_size = 0.1
    layer_objectdata.empty_display_type = 'PLAIN_AXES'

    cell_collection.objects.link(layer_objectdata)

    for poly in layer["polygons"]:
        
        curvedata = D.curves.new(name='Curve', type='CURVE')
        curvedata.dimensions = '2D'
        curvedata.fill_mode = 'BOTH'
        curvedata.name = obj_name
        
        objectdata = D.objects.new(obj_name, curvedata)
        objectdata.location = (0,0,0) #object origin
        objectdata.parent = layer_objectdata
        # objectdata.data.materials.append(net_material)
        cell_collection.objects.link(objectdata)
        layer_objects[layer_id].append(objectdata)
        

        current_z = 0
        curvedata.extrude = 0.05 #50*SCALE
        
        
            
        polyline = curvedata.splines.new('POLY')
        
        polyline.points.add(len(poly)-1)

        for num in range(len(poly)):
            x, y, z = poly[num][0] * SCALE, poly[num][1] * SCALE, current_z
            
            # px,py,pz = current_x+x, current_y+y, z
            # current_x, current_y = px, py                
            # polyline.points[num].co = (px, py, pz, w)
            polyline.points[num].co = (x, y, z, 1)

            
        polyline.use_cyclic_u = 1
        #polyline.use_cyclic_v = 1
        polyline.use_smooth = False
        

    for label in layer["labels"]:
        text = label["text"]
        txt_data = D.curves.new(name=text, type='FONT')
        # Text Object
        txt_ob = D.objects.new(name="Text_"+text, object_data=txt_data)
        txt_ob.parent = layer_objectdata
        
        txt_ob.location[0] = label["position"][0] * SCALE
        txt_ob.location[1] = label["position"][1] * SCALE
        #txt_ob.location[2] = 0.61
        
        cell_collection.objects.link(txt_ob)   # add the data to the scene as an object
        layer_objects[layer_id].append(txt_ob)
        
        txt_data.body = text         # the body text to the command line arg given
        txt_data.align_x = 'CENTER'  # center text
        txt_data.align_y = 'CENTER'  # center text
        txt_data.size = 0.15




i = 0.0
for obj in cell_collection.objects:
    if (obj.type=="EMPTY"):        
        # obj.location.z = i
        obj_name = obj.name.lower()
        gds_layer_name = obj_name
        
        if(obj_name.find(".")>0):
            gds_layer_name = obj_name[:obj_name.find(".")]

        print(gds_layer_name)
        
        if(D.objects.find("TEMPL_" + gds_layer_name)!=-1):
            obj.location = D.objects["TEMPL_"+gds_layer_name].location
            obj.scale = D.objects["TEMPL_"+gds_layer_name].scale
            # obj.data.materials.append(D.objects["TEMPL_"+gds_layer_name].data.materials[0])
            obj.select_set(True)
            # C.view_layer.objects.active = obj
            
            for child in obj.children:
                child.data.materials.append(D.objects["TEMPL_"+gds_layer_name].children[0].data.materials[0])
                child.select_set(True)



D.collections["TEMPLATE"].hide_render = True
D.collections["TEMPLATE"].hide_viewport = True

bpy.ops.view3d.camera_to_view_selected()


CELL_NAME = os.path.basename(input_cell_json_path).split(".")[0]





cell_width = (cell["bounding_box"][1][0]-cell["bounding_box"][0][0]) * SCALE
cell_height = (cell["bounding_box"][1][1]-cell["bounding_box"][0][1]) * SCALE
resolution_ratio = C.scene.render.resolution_x / C.scene.render.resolution_y

# Setup cameras to view the cells
for obj in C.scene.objects:
    if obj.type == 'CAMERA':
        C.scene.camera = obj
        bpy.ops.view3d.camera_to_view_selected()    
        if(obj.name=="RIGHT"):            
            D.cameras[obj.data.name].ortho_scale = cell_height
        elif(obj.name=="FRONT"):
            D.cameras[obj.data.name].ortho_scale = cell_width
        elif(obj.name=="TOP"):
            if(cell_width>=cell_height*resolution_ratio):
                D.cameras[obj.data.name].ortho_scale = cell_width
            else:
                D.cameras[obj.data.name].ortho_scale = cell_height*resolution_ratio

            

def executeRender(filename, render) : 
    render.image_settings.file_format = 'JPEG' #'PNG'
    render.use_file_extension
    render.resolution_percentage = RESOLUTION_PERCENTAGE
    render.use_file_extension = True
    render.filepath = filename

    print("Rendering "+filename + " ...")
    bpy.ops.render.render(write_still=True, use_viewport=False)

def changeLayersVisibility(layer_id_array, hide=True):
    for lid in layer_id_array:
        if(lid in layer_objects):
            for obj in layer_objects[lid]:
                obj.hide_viewport = hide
                obj.hide_render = hide


# Renders
for obj in C.scene.objects:
    if obj.type == 'CAMERA':
        C.scene.camera = obj


        filename = os.path.join(output_path, CELL_NAME + "_" + C.scene.camera.name + ".png")
        executeRender(filename, C.scene.render)

        
        # SKY130 Example of doing more renders disabling some layers
        if(False):
            # Hide all metal related layers
            changeLayersVisibility([
                    "72/20", "72/16", "72/5",
                    "71/44", "71/20", "71/16", "71/5",
                    "70/44", "70/20", "70/16", "70/5",
                    "69/44", "69/20", "69/16", "69/5",
                    "68/44", "68/20", "68/16", "68/5", 
                    "67/44"
                    ], hide=True)
                

            filename = CELL_NAME + "_" + C.scene.camera.name + "-NO-met1.png"
            executeRender(filename, C.scene.render)


            
            # Hide li1 related layers
            changeLayersVisibility(["67/20", "67/16", "67/5"], hide=True)
                
            filename = CELL_NAME + "_" + C.scene.camera.name + "-NO-met1-No-li1.png"
            executeRender(filename, C.scene.render)

            # Show all metal related layers
            changeLayersVisibility([
                    "72/20", "72/16", "72/5",
                    "71/44", "71/20", "71/16", "71/5",
                    "70/44", "70/20", "70/16", "70/5",
                    "69/44", "69/20", "69/16", "69/5",
                    "68/44", "68/20", "68/16", "68/5", 
                    "67/44"
                    ], hide=False)
            
            
            # Show li1 related layers
            changeLayersVisibility(["67/20", "67/16", "67/5"], hide=False)
            

