#!/bin/env python3

from lib.youtube.youtube import YouTube

class PlaylistItem:

    SNIPPET_KEY='snippet'
    PARTS=(SNIPPET_KEY,)

    def __init__(self):
        self.body = {
            self.SNIPPET_KEY: {}
        }

    def setPlaylistId(self, playlistId: str):
        self.body[self.SNIPPET_KEY]['playlistId'] = playlistId

    def setVideoId(self, videoId: str):
        self.body[self.SNIPPET_KEY]['resourceId'] = dict(
            kind='youtube#video',
            videoId=videoId
        )

    def insert(self):
        ret = YouTube().get().playlistItems().insert(
            part=','.join(self.PARTS),
            body=self.body
        ).execute()

    @staticmethod
    def createFromSearchResult(res):
        pl = PlaylistItem()
        pl.setVideoId(res['items'][0]['id']['videoId'])
        return pl
