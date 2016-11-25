"""
Core logic for Race Manager.

The requests module is used for HTTP communications with the Race Monitor API.
PIP can be used to install requests if it is needed for development. "pip install requests"

wxPython 3.x is used for the windowing toolkit. QT was considered but there is no version of
PySide 1.2x for Python 3.5 and PySide 2.x is, as of November 2016, not ready for production use.
The wxPython 3.x binary builds can be found here, https://wxpython.org/Phoenix/snapshot-builds/

**Author:**

	Jeff Hanna, 11/22/2016
"""

import os
import requests

import const


# Filepath of a text file containing the Race Monitor issued developer API token.
# This token is intentionally kept out of the Visual Studio solution and ignored by GIT 
# to keep the token private. Any developers contibuting to this program will need to get their
# own API token and use that.
#
# THIS WILL NEED TO BE REPLACED WITH A RACE MONITOR ISSUED COMMERCIAL API TOKEN BEFORE THE 
# SOFTWARE IS BUILT FOR COMMERCIAL DISTRIBUTION.
_API_TOKEN_FILEPATH = os.path.abspath( os.path.join( os.getcwd( ), 'api_token.txt' ) )
	

def get_api_token( ) -> str:
	"""
	Gets the Race Monitor issued api token for this application.
	The api token is stored in an external file named 'api_token.txt'. That file is not
	sync'd to the GIT repository so that the token remains secure.

	**Arguments:**
		
		None

	**Keyword Arguments:**

		None

	**Author:**

		Jeff Hanna, 11/24/2016
	"""

	if os.path.exists( _API_TOKEN_FILEPATH ):
		with open( _API_TOKEN_FILEPATH, 'r' ) as file:
			api_token = file.readline( ).rstrip( )

	return api_token or ''
	

def get_app_sections( ) -> list:
	"""
	Retrieves the list of app sections from the Race Monitor servers.

	**Arguments:**
		
		None

	**Keyword Arguments:**

		None

	**Author:**

		Jeff Hanna, 11/22/2016
	"""

	url = 'https://api.race-monitor.com/v2/Common/AppSections'
	api_token = get_api_token( )
	
	if api_token:
		post_data = { const.API_TOKEN_KEY : api_token }
		data = requests.post( url, post_data )
		data = data.json( )
	
		success = data.get( const.API_SUCCESSFUL_KEY, False )
		if success:
			app_sections = data.get( const.API_APP_SECTIONS_KEY, [ ] )

	return app_sections or [ ]
