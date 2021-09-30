# GDSPY docs:
#   https://gdspy.readthedocs.io/en/stable/index.html

import sys # read command-line arguments
import os
import json
import gdspy # open gds file
import argparse


argparser = argparse.ArgumentParser(description='Convert GDSII files into json.')
argparser.add_argument('-l', "--layerstack_file", required=True, help="Layer stack json file")
argparser.add_argument('-g', "--gds_file", required=True, help="GDS file")
argparser.add_argument('-o', "--output_path", required=False, help="Path to put the generated json files")


args = vars(argparser.parse_args())


def create_layer(layerid):
    global layerstack
    layer = {"name" : "", "polygons":[], "labels" : []}
    if(layerid in layerstack):
        layer["name"] = layerstack[layerid]    
    return layer



layerstack_file_path = args["layerstack_file"]
gdsii_file_path = args["gds_file"]

if(args["output_path"]==None):    
    output_file_path = os.path.dirname(gdsii_file_path)
else:
    output_file_path = args["output_path"]

    try:
        os.makedirs(output_file_path, exist_ok = True)
        #print("Output directory '%s' created successfully" % output_file_path)
    except OSError as error:
        print("Output directory '%s' can not be created" % output_file_path)
        exit()


 




layerstack_file = open(layerstack_file_path, "r")
layerstack = json.load(layerstack_file)
layerstack_file.close()

print(layerstack)


print('Reading GDSII file {}...'.format(gdsii_file_path))
gdsii = gdspy.GdsLibrary()
gdsii.read_gds(gdsii_file_path, units='import')


output_layers = {}

# cells = gdsii.top_level() # get all cells that aren't referenced by another
for cell in gdsii: # loop through cells to read paths and polygons
    
    output_layers = {}

    # $$$CONTEXT_INFO$$$ is a separate, non-standard compliant cell added
    # optionally by KLayout to store extra information not needed here.
    # see https://www.klayout.de/forum/discussion/1026/very-
    # important-gds-exported-from-k-layout-not-working-on-cadence-at-foundry
    if cell.name == '$$$CONTEXT_INFO$$$':
        continue # skip this cell

    # combine will all referenced cells (instances, SREFs, AREFs, etc.)
    cell = cell.flatten()


    # Polygons
    layers = cell.get_polygons(True)
    for id, polygons in layers.items():
        layerid = str(id[0]) + "/" + str(id[1])
        
        if(not layerid in output_layers):
            output_layers[layerid] = create_layer(layerid)

        for poly in polygons:
            output_layers[layerid]["polygons"].append(poly.tolist())


    # Labels
    labels = cell.get_labels()    
    for label in labels:
        layerid = str(label.layer) + "/" + str(label.texttype)

        if(not layerid in output_layers):
            output_layers[layerid] =  create_layer(layerid)

        
        output_layers[layerid]["labels"].append( {"text":label.text, "position" : label.position.tolist(), "anchor": label.anchor , "rotation":label.rotation, "magnification": label.magnification, "x_reflection": label.x_reflection } )




    # Write Cell json
    output_filename = cell.name + ".json"

    cell_output = {"name" : cell.name , "bounding_box" : cell.get_bounding_box().tolist(), "layers" : output_layers}

    print("Writing", output_filename,  "...")
    output_json_file = open(os.path.join(output_file_path, output_filename), "w")
    json.dump(cell_output, output_json_file)
    output_json_file.close()


