# -*- encoding: utf-8 -*-
"""
Copyright (c) 2019 - present AppSeed.us
"""
import json

from flask_migrate import Migrate
from os import environ
from sys import exit
from decouple import config
import logging

from config import config_dict
from app import create_app, db

# WARNING: Don't run with debug turned on in production!
DEBUG = config('DEBUG', default=True, cast=bool)

# The configuration
get_config_mode = 'Debug' if DEBUG else 'Production'

try:
    
    # Load the configuration using the default values 
    app_config = config_dict[get_config_mode.capitalize()]

except KeyError:
    exit('Error: Invalid <config_mode>. Expected values [Debug, Production] ')

app = create_app( app_config ) 
Migrate(app, db)

if DEBUG:
    app.logger.info('DEBUG       = ' + str(DEBUG)      )
    app.logger.info('Environment = ' + get_config_mode )
    app.logger.info('DBMS        = ' + app_config.SQLALCHEMY_DATABASE_URI )


def tone_analyzer():
    from ibm_watson import ToneAnalyzerV3
    from ibm_cloud_sdk_core.authenticators import IAMAuthenticator

    #authenticator = IAMAuthenticator('')
    tone_analyzer = ToneAnalyzerV3(
        version='2017-09-21',
        authenticator=authenticator
    )

    tone_analyzer.set_service_url('https://api.us-south.tone-analyzer.watson.cloud.ibm.com/instances/1ff8997b-7f27-4424-99a2-514475e44d41/v3/tone?version=2017-09-21')
    text = 'Team, I know that times are tough! Product ' \
           'sales have been disappointing for the past three ' \
           'quarters. We have a competitive product, but we ' \
           'need to do a better job of selling it!'\
           'I am sure we can do it! We did it before and we can do it now! '

    tone_analysis = tone_analyzer.tone(
        {'text': text},
        content_type='application/json',
        sentences= True
    ).get_result()
    print(json.dumps(tone_analysis, indent=2))



if __name__ == "__main__":
    #tone_analyzer()
    app.run(port=5070)
