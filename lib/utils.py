#!/bin/env python3

import json, os

from lib.youtube.playlist import Playlist

def load_playlists_json_file(fname):
    raw_playlists = []
    with open(fname) as f:
        raw_playlists = json.load(f)
    playlists = [Playlist.createFromDict(pl) for pl in raw_playlists]
    _sync_playlist_sequences(_recover_playlist_videos,
                             raw_playlists,
                             playlists)
    return playlists

def _sync_playlist_sequences(func, raw_playlists: dict, playlists):
    for rpl, pl in zip(raw_playlists, playlists):
        func(rpl, pl)

def _recover_playlist_videos(raw_playlist: dict, playlist):
    for search_query in raw_playlist.get('videos', ()):
        playlist.addSearchItem(search_query)

def store_playlists_json_file(fname, playlists):
    raw_playlists = [i.getBodyDictCopy() for i in playlists]
    _sync_playlist_sequences(_store_playlist_videos,
                             raw_playlists,
                             playlists)
    with open(fname, 'w') as f:
        json.dump(raw_playlists, f)
    return

def _store_playlist_videos(raw_playlist: dict, playlist):
    raw_playlist['videos'] = playlist.getSearchItemsCopy()

def apply_cmdline_settings_to_playlist(playlist, settings):
    playlist.setTitle(settings['title'])
    if settings['description'] is not None:
        playlist.setDescription(settings['description'])
    if settings['privacyStatus'] is not None:
        playlist.setPrivacyStatus(settings['privacyStatus'])
    if settings['videoid'] is not None:
        [playlist.addSearchItem(vid) for vid in settings['videoid']]
    return playlist

