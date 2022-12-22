#!/bin/sh
OUTPUT_PATH="./example_renders/sky130_fd_sc_hvl-latest/"
SCALE=1.0

for file in ./gds/sky130_fd_sc_hvl-json/*.json
do
	blender -b ./blender/TEMPLATE_SKY130_LIBRARY_CELLS.blend  -P ./scripts/library_cell_render.py  -- -i $file -o $OUTPUT_PATH -s $SCALE
done
