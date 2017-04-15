#!/bin/env python3

import json, argparse, os

from lib.utils import (load_playlists_json_file,
                       store_playlists_json_file,
                       apply_cmdline_settings_to_playlist)
from lib.youtube.playlist import Playlist

def get_cmd_line_parser():
    if not hasattr(get_cmd_line_parser, "args_parser"):
        args_parser = argparse.ArgumentParser()
        args_parser.add_argument("-t", "--title", required=True)
        args_parser.add_argument("-n", "--num", type=int)
        args_parser.add_argument("-d", "--description")
        args_parser.add_argument("-s", "--privacy-status",
                                 dest='privacyStatus',
                                 choices=["private", "public", "unlisted"],
                                 default="private")
        args_parser.add_argument("-v", "--videoid", nargs="+")
        args_parser.add_argument("-f", "--filename", default="input.json")
        get_cmd_line_parser.args_parser = args_parser
    return get_cmd_line_parser.args_parser

def get_cmd_line_settings():
    return get_cmd_line_parser().parse_args()

class InputFile:
    def __init__(self, cmd_line_settings):
        self.settings = vars(cmd_line_settings)
        self.playlists = []
        self.output_file = None

    def applySettings(self):
        if self.settings['filename'] is not None:
            if os.path.exists(self.settings['filename']):
                self.playlists = load_playlists_json_file(
                    self.settings['filename']
                )
            self.output_file = self.settings['filename']

        playlist = None
        if self.settings['num'] is not None:
            playlist = self.playlists[self.settings['num']]
        else:
            playlist = Playlist()
            self.playlists.append(playlist)

        apply_cmdline_settings_to_playlist(playlist, self.settings)

    def store(self):
        store_playlists_json_file(self.settings['filename'], self.playlists)

if __name__ == '__main__':
    cmd_line_settings = get_cmd_line_settings()

    inp_file = InputFile(cmd_line_settings)
    inp_file.applySettings()
    inp_file.store()
