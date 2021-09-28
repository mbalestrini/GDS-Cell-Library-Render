import bpy
from bpy.types import LayerCollection, Material
import sys # read command-line arguments
import os
import json 


D = bpy.data
C = bpy.context

# SETTINGS
#SCALE = 0.001
SKIP_UNNAMED_LAYERS = True



if(len(sys.argv)>1):
    # last arguments is the cell json file
    input_cell_json_path = sys.argv[len(sys.argv)-1]
else:
    print("hardcoded import file for testing")



cell_file = open(input_cell_json_path, "r")
cell = json.load(cell_file)
cell_file.close()


print("Cell Layers:")
for layer_id, layer in cell.items():
    print(layer_id, layer["name"], "polygons", len(layer["polygons"]))





# Create "CELL" collection and link it
cell_collection = D.collections.new("CELL")
C.scene.collection.children.link(cell_collection)


# Select "CELL" as active collection
collections = bpy.context.view_layer.layer_collection.children
for collection in collections:
    if collection.name == "CELL":
        bpy.context.view_layer.active_layer_collection = collection




for layer_id, layer in cell.items():
    if(SKIP_UNNAMED_LAYERS and layer["name"]==""):
        continue
    # if(not layer_id in ("64/20", "65/20", "66/20", "67/20", "68/20", "69/20", "70/20", "71/20", "72/20")):
        # continue

    print("Importing layer",  layer_id, layer["name"])

    material_name = layer_id

    # net_material = D.materials.new(material_name)

    obj_name = layer_id + "_" + layer["name"]

    layer_objectdata = D.objects.new( obj_name, None )
    # empty_draw was replaced by empty_display
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

        current_z = 0
        curvedata.extrude = 0.05 #50*SCALE
        
        
            
        polyline = curvedata.splines.new('POLY')
        
        polyline.points.add(len(poly)-1)

        for num in range(len(poly)):
            x, y, z = poly[num][0], poly[num][1], current_z
            
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
        
        txt_ob.location[0] = label["position"][0]
        txt_ob.location[1] = label["position"][1]
        #txt_ob.location[2] = 0.61
        
        cell_collection.objects.link(txt_ob)   # add the data to the scene as an object
        
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

for obj in C.scene.objects:
    if obj.type == 'CAMERA':
        C.scene.camera = obj
        bpy.ops.view3d.camera_to_view_selected()    
       
        filename = CELL_NAME + "_" + C.scene.camera.name + ".png"
        render = C.scene.render
        render.image_settings.file_format = 'JPEG' #'PNG'
        render.use_file_extension
        render.resolution_percentage = 50
        render.use_file_extension = True
        # render.filepath = os.path.join(CELL_PATH, filename)
        render.filepath = "./renders/" + filename

        print("Rendering "+filename + " ...")
        bpy.ops.render.render(write_still=True, use_viewport=False)
