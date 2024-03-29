# GDS Cell Library Render

More than a proper tool this repo is more oriented to help people find out how to make some GDS blender renders similar to what is in the `examples_render` folders


## Requirements
Tested on linux, with `python 3.6.9` and `blender 2.91`

For running the `gds_to_json.py` script you need `gdspy` module (tested on 1.6.6 version)

## Usage

ELABORATE: Render script needs gds json files

ELABORATE: Alternatively you can use the TEMPLATE_XXXX.blender files as an example to do your own GDS/MAGIC parser

ELABORATE: How to run the script internally in blender with some json file

ELABORATE: Internal parameters at the beginning of the `library_cell_render.py` file (ex: changing render resolution)

TODO: example call to `gds_to_json.py`

TODO: example render call (`./run_sky130_fd_sc_hd__renders.sh` )


---

## Example Renders

`sky130_fd_sc_hd__inv_2` top view:
![sky130_fd_sc_hd__inv_2 cell render. top view](example_renders/sky130_fd_sc_hd-latest/sky130_fd_sc_hd__inv_2_TOP.jpg)

`gf180mcu_fd_sc_mcu7t5v0__inv_1` top view:
![gf180mcu_fd_sc_mcu7t5v0__inv_1 cell render. top view](example_renders/gf180mcu_fd_sc_mcu7t5v0-latest/gf180mcu_fd_sc_mcu7t5v0__inv_1_TOP.jpg)


`sky130_fd_sc_hd__mux2_1` perspective view:
![sky130_fd_sc_hd__mux2_1 cell render. perspective view](example_renders/sky130_fd_sc_hd-latest/sky130_fd_sc_hd__mux2_1_PERSPECTIVE.jpg)


`gf180mcu_fd_sc_mcu7t5v0__buf_4` perspective view:
![gf180mcu_fd_sc_mcu7t5v0__buf_4 cell render. perspective view](example_renders/gf180mcu_fd_sc_mcu7t5v0-latest/gf180mcu_fd_sc_mcu7t5v0__buf_4_PERSPECTIVE.jpg)


