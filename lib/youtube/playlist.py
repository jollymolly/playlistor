#!/bin/env python3

from lib.youtube.playlistitem import PlaylistItem
from lib.youtube.youtube import YouTube
from lib.youtube.search import Search

class Playlist:

    ID_KEY = 'id'
    SNIPPET_KEY = 'snippet'
    TITLE_KEY = 'title'
    DESCRIPTION_KEY = 'description'
    STATUS_KEY = 'status'
    PRIVACYSTATUS_KEY = 'privacyStatus'

    def __init__(self):
        self.body = {
            self.SNIPPET_KEY: dict(),
            self.STATUS_KEY: dict(),
        }
        self.playlistItems = []
        self.searchItems = []

    def setTitle(self, title: str):
        if title is None:
            raise ValueError("Playlist: title should provided")
        self.body[self.SNIPPET_KEY][self.TITLE_KEY] = title

    def setDescription(self, description: str):
        self.body[self.SNIPPET_KEY][self.DESCRIPTION_KEY] = description

    def setPrivacyStatus(self, privacyStatus: str):
        privacyStatus = privacyStatus if privacyStatus else 'private'
        if privacyStatus not in ('private', 'public', 'unlisted'):
            raise ValueError("Playlist: wrong privacy status value(%s)" %
                            privacystatus)
        self.body[self.STATUS_KEY][self.PRIVACYSTATUS_KEY] = privacyStatus

    def addItem(self, plItem):
        self.playlistItems.append(plItem)

    def addSearchItem(self, search_query: str):
        self.searchItems.append(search_query)

    def __processSearchItems(self):
        for si in self.searchItems:
            res = Search.search(si)
            plI = PlaylistItem.createFromSearchResult(res)
            if self.ID_KEY in self.body:
                plI.setPlaylistId(self.body[self.ID_KEY])
            self.playlistItems.append(plI)
        self.searchItems = []

    def getSearchItemsCopy(self):
        return list(self.searchItems)

    def insert(self):
        ret = YouTube().get().playlists().insert(
            part=','.join(self.body.keys()),
            body=self.body
        ).execute()

        self.body[self.ID_KEY] = ret[self.ID_KEY]
        self.__processSearchItems()
        for plItem in self.playlistItems:
            plItem.insert()
        return

    @staticmethod
    def createFromDict(d: dict):
        pl = Playlist()
        if Playlist.SNIPPET_KEY in d:
            pl.setTitle(d[Playlist.SNIPPET_KEY].get(Playlist.TITLE_KEY, None))
            pl.setDescription(d[Playlist.SNIPPET_KEY].get(
                Playlist.DESCRIPTION_KEY, None))
        if Playlist.STATUS_KEY in d:
            pl.setPrivacyStatus(d[Playlist.STATUS_KEY].get(
                Playlist.PRIVACYSTATUS_KEY, None))
        return pl

    def getBodyDictCopy(self):
        return dict(self.body)
