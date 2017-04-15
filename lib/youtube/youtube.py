#!/bin/env python3

import httplib2
import os
import sys
import json

from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.client import flow_from_clientsecrets
from oauth2client.file import Storage
from oauth2client.tools import run_flow

from lib.playlistor.utils import get_cmd_line_parser
from lib.settings import Settings


class YouTube:
    __instance = None

    YOUTUBE_READ_WRITE_SCOPE = "https://www.googleapis.com/auth/youtube"
    YOUTUBE_API_SERVICE_NAME = "youtube"
    YOUTUBE_API_VERSION = "v3"
    MISSING_CLIENT_SECRETS_MESSAGE = "Error: {}\nFor more information about\
 the client_secrets.json file format, please visit:\n\
https://developers.google.com/api-client-library/python/guide/\
aaa_client_secrets"

    def __new__(cls):
        if YouTube.__instance is None:
            YouTube.__instance = super().__new__(cls)
        return YouTube.__instance

    def __init__(self):
        self.yt = None

    def __setup(self):
        flow = flow_from_clientsecrets(Settings.getSecret(),
                                       message=self.MISSING_CLIENT_SECRETS_MESSAGE,
                                       scope=self.YOUTUBE_READ_WRITE_SCOPE)
        storage = Storage("%s-oauth2.json" % sys.argv[0])
        credentials = storage.get()

        if credentials is None or credentials.invalid:
            flags = get_cmd_line_parser().parse_args()
            credentials = run_flow(flow, storage, flags)

        self.yt = build(self.YOUTUBE_API_SERVICE_NAME,
                        self.YOUTUBE_API_VERSION,
                        http=credentials.authorize(httplib2.Http()))
        return self.yt

    def get(self):
        return self.yt if self.yt else self.__setup()
