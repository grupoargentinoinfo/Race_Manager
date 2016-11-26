import getpass
import os
import sys

username = getpass.getuser( )

platform = sys.platform.lower( )
if platform == 'win32':
  DATA_DIR = os.path.abspath( os.path.join( os.getenv( 'LOCALAPPDATA' ), 'race_manager' ) )
elif platform in [ 'darwin', 'linux' ]:
  DATA_DIR = os.path.abspath( os.path.join( os.path.expanduser( '~{0}'.format( username ) ) ) )

if not os.path.exists( DATA_DIR ):
	os.mkdir( DATA_DIR )

PREFS_FILEPATH = os.path.abspath( os.path.join( DATA_DIR, 'prefs.json' ) )

MAIN_FRAME_TITLE = 'Race Managger'
MAIN_FRAME_DEFAULT_SIZE = ( 1024, 768 )
MAIN_FRAME_DEFAULT_POSITION = ( -1, -1 )

RACE_SELECTION_DLG_TITLE = 'Select a Race Type'
RACE_SELECTION_DLG_DEFAULT_POSITION = ( -1, -1 )
RACE_SELECTION_DLG_DEFAULT_SIZE = ( 915, 660 )

API_TOKEN_KEY = 'apiToken'
API_SERIES_ID_KEY = 'seriesID'
API_SUCCESSFUL_KEY = 'Successful'
API_APP_SECTIONS_KEY = 'AppSections'
API_RACES_KEY = 'Races'
API_NAME_KEY = 'Name'
API_IMAGES_KEY = 'Images'
API_ID_KEY = 'ID'
NAME_IGNORE_LIST = [ 'Oval Racing', ]