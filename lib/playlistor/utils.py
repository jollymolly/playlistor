#!/bin/env python3

import argparse

from oauth2client.tools import argparser

def get_cmd_line_parser():
    if not hasattr(get_cmd_line_parser, 'args_parser'):
        args_parser = argparse.ArgumentParser(parents=[argparser])
        args_parser.add_argument("input")
        get_cmd_line_parser.args_parser = args_parser
    return get_cmd_line_parser.args_parser

def get_cmd_line_settings():
    return get_cmd_line_parser().parse_args()
