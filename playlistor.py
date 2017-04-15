#!/bin/env python3

from lib.utils import load_playlists_json_file
from lib.playlistor.utils import get_cmd_line_settings

if __name__ == '__main__':
    cmd_line_settings = get_cmd_line_settings()
    playlists = load_playlists_json_file(cmd_line_settings.input)
    for pl in playlists:
        pl.insert()
