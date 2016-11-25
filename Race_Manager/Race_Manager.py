"""
Race stratgy manager that utilizes Race Monitor data streams.
**Author:**

	Jeff Hanna, 11/22/2016
"""

import io
import os
import requests


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
	

def get_app_sections( url: str, api_token: str ) -> list:
	"""
	Retrieves the list of app sections from the Race Monitor servers.

	**Arguments:**
		
		:``url``: `string` The race monitor URL
		:``api_token: `string` The Race Monitor issued api token for this application.

	**Keyword Arguments:**

		None

	**Author:**

		Jeff Hanna, 11/22/2016
	"""

	post_data = { 'apiToken': api_token }
	data = requests.post( url, post_data )
	data = data.json( )
	
	success = data.get( 'Successful', False )
	if success:
		app_sections = data.get( 'AppSections', [ ] )

	return app_sections or [ ]


def list_section_names( app_sections: dict ):
	# This should built app section classes.
	for x in app_sections:
		print( x.get( 'Name', '' ) )


def main( ) -> None:
	"""
	The main function for this application.

	**Arguments:**
		
		None

	**Keyword Arguments:**

		None

	**Author:**

		Jeff Hanna, 11/24/2016
	"""

	_URL = 'https://api.race-monitor.com/v2/Common/AppSections'
	_API_TOKEN = get_api_token( )
	if _API_TOKEN:
		app_sections = get_app_sections( _URL, _API_TOKEN )
		list_section_names( app_sections )
	else:
		print( 'No valid API token was found. Cannot continue.' )



if __name__ == '__main__':
	main( )