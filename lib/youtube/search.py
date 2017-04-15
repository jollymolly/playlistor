#!/bin/env python3

from lib.youtube.youtube import YouTube

class Search:

    SNIPPET_KEY='snippet'
    PARTS=('id', SNIPPET_KEY)

    @staticmethod
    def search(search_query):
        ret = YouTube().get().search().list(
            q=search_query,
            type="video",
            part=','.join(Search.PARTS),
            maxResults=1
        ).execute()

        return ret
