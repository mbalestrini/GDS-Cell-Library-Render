#!/bin/sh
OUTPUT_PATH="./renders/librecell-latest/"
SCALE=0.1

for file in ./gds/librecell-json/*.json
do
	blender -b ./blender/TEMPLATE_LIBRECELL_LIBRARY_CELLS.blend  -P ./scripts/library_cell_render.py  -- -i $file -o $OUTPUT_PATH -s $SCALE
done
