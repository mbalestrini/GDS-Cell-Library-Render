#!/bin/sh

for file in ./gds/json/*.json
do
	blender -b ./blender/TEMPLATE_SKY130_LIBRARY_CELLS.blend  -P ./scripts/sky130_lib_render.py  -- $file
done
