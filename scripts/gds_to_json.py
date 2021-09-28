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
print(args)


# # get the input file name
# if len(sys.argv) < 2: # sys.argv[0] is the name of the program
#     print("Error: need exactly one file as a command line argument.")
#     sys.exit(0)
#gdsii_file_path = sys.argv[1]


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
    print("Writing", output_filename,  "...")
    output_json_file = open(os.path.join(output_file_path, output_filename), "w")
    json.dump(output_layers, output_json_file)
    output_json_file.close()


#res[list(res.keys())[3]][0].tolist()