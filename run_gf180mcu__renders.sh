#!/bin/sh
OUTPUT_PATH="./example_renders/gf180mcu_fd_sc_mcu7t5v0-latest/"
SCALE=1.0

for file in ./gds/gf180mcu_fd_sc_mcu7t5v0-json/*.json
do
	blender -b ./blender/TEMPLATE_GF180MCU_LIBRARY_CELLS.blend  -P ./scripts/library_cell_render.py  -- -i $file -o $OUTPUT_PATH -s $SCALE
	# blender -b ./blender/TEMPLATE_GF180MCU_LIBRARY_CELLS.blend  -P ../GDS_and_Blender/scripts/library_cell_render.py  -- -i $file -o $OUTPUT_PATH -s $SCALE
done
