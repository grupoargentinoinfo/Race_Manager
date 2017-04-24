# -*- coding: utf-8 -*- 

import getpass
import os
import sys


APP_NAME = 'Race Manager'

# Get around developer API rate limit by using locally stored json data
USE_LOCAL_DATA = True

# SETUP PREFERENCES DIRECTORY FILEPATH
username = getpass.getuser( )

platform = sys.platform.lower( )
if platform == 'win32':
  DATA_DIR = os.path.abspath( os.path.join( os.getenv( 'LOCALAPPDATA' ), 'race_manager' ) )
elif platform in [ 'darwin', 'linux' ]:
  DATA_DIR = os.path.abspath( os.path.join( os.path.expanduser( '~{0}'.format( username ) ) ) )

if not os.path.exists( DATA_DIR ):
	os.mkdir( DATA_DIR )

PREFS_FILEPATH = os.path.abspath( os.path.join( DATA_DIR, 'prefs.json' ) )

# API TOKEN INFORMATION
# Filepath of a text file containing the Race Monitor issued developer API token.
# This token is intentionally kept out of the Visual Studio solution and ignored by GIT 
# to keep the token private. Any developers contibuting to this program will need to get their
# own API token and use that.
#
# THIS WILL NEED TO BE REPLACED WITH A RACE MONITOR ISSUED COMMERCIAL API TOKEN BEFORE THE 
# SOFTWARE IS BUILT FOR COMMERCIAL DISTRIBUTION.
__API_TOKEN_FILEPATH = os.path.abspath( os.path.join( os.getcwd( ), 'api_token.txt' ) )


RACE_MONITOR_URL = 'https://api.race-monitor.com/v2/'

MAIN_FRAME_DEFAULT_SIZE = ( 1024, 768 )
MAIN_FRAME_DEFAULT_POSITION = ( -1, -1 )

RACE_SELECTION_DLG_DEFAULT_POSITION = ( -1, -1 )
RACE_SELECTION_DLG_DEFAULT_SIZE = ( 550, 450 )

API_APP_SECTIONS_KEY = 'AppSections'
API_COMPETITORS_KEY = 'Competitors'
API_ID_KEY = 'ID'
API_IMAGES_KEY = 'Images'
API_IS_LIVE_KEY = 'IsLive'
API_MESSAGE_KEY = 'Message'
API_RACE_NAME_KEY = 'Name'
API_RACE_ID_KEY = 'raceID'
API_RACES_KEY = 'Races'
API_SERIES_ID_KEY = 'seriesID'
API_SESSION_ID_KEY = 'sessionID'
API_SESSION_KEY = 'Session'
API_SUCCESSFUL_KEY = 'Successful'
API_TOKEN_KEY = 'apiToken'
API_RATE_LIMIT_EXCEEDED_KEY = 'Rate limit exceeded'

NAME_IGNORE_LIST = [ 'Oval Racing', ]

STOPWATCH_DEFAULT_VALUE = '0:00:00.000'