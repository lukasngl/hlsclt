# -*- coding: utf-8 -*-
""" Helper functions for the HLSCLT Command Line Tool.

Copyright (c) 2017 Ben Marshall
"""

import os
from pyaml import yaml
from glob import glob
from .classes import Error
from .config import parse_and_map, parse_choice, parse_default, parse_dict
from .config import parse_int, parse_list, parse_one_of, parse_string

def load_config(file):
    """
    Function to load the configuration from a file.
    """
    config_file = read_config_file(file)
    parsed = get_config_parser()(file.name, config_file)
    # Context sensitive analysis
    if isinstance(parsed, Error):
        raise parsed
    return parsed


def config_parser():

    default_proj_name = parse_default("proj_%s" % os.path.relpath(".", ".."))

    return parse_dict({
        "project_name": parse_one_of(parse_string,
                                     default_proj_name),
        "top_level_function_name": parse_string,
        "src_dir_name": parse_one_of(parse_string,
                                     parse_default("src/")),
        "tb_dir_name": parse_one_of(parse_string,
                                    parse_default("tb/")),
        "src_files": parse_one_of(parse_list(parse_string),
                                  parse_default([])),
        "tb_files": parse_one_of(parse_list(parse_string),
                                 parse_default([])),
        "compiler": parse_one_of(parse_choice("gcc", "clang"),
                                 parse_default("gcc")),
        "part_name": parse_string,
        "clock_period": parse_int,
        "language": parse_one_of(parse_choice("vhdl", "verilog"),
                                 parse_default("vhdl")),
    })


# Function to find the highest solution number within a HLS project.
def find_solution_num(ctx):
    config = ctx.obj.config
    # Seach for solution folders
    paths = glob(config["project_name"] + "/solution*/")
    solution_num = len(paths)
    # First solution is always 1.
    if solution_num == 0:
        solution_num = 1;
    else:
        # Only if this isn't the first solution
        # If keep argument is specified we are starting a new solution.
        try:
            if ctx.params["keep"]:
                solution_num = solution_num + 1
        except KeyError:
            pass
    return solution_num
