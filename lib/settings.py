#!/bin/env python3

import os

class Settings:

    CLIENT_SECRET_ENV_VAR_NAME = 'YT_CLIENT_SECRET'

    @staticmethod
    def getSecret():
        if os.environ.get(Settings.CLIENT_SECRET_ENV_VAR_NAME, None) is None:
            raise ValueError('YT_CLIENT_SECRET: env var must be defined'
                              ' pointing to a valid secret file')
        elif not os.path.exists(
                os.environ[Settings.CLIENT_SECRET_ENV_VAR_NAME]):
            raise ValueError('YT_CLIENT_SECRET(%s): does not exist' %
                              os.environ[Settings.CLIENT_SECRET_ENV_VAR_NAME])

        return os.environ[Settings.CLIENT_SECRET_ENV_VAR_NAME]
