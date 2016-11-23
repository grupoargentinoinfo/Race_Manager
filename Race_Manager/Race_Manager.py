'''
MODULE LEVEL DOCSTRING GOES HERE
'''

import os
import urllib.request
import urllib.parse


_API_TOKEN_FILEPATH = os.path.abspath( os.path.join( os.getcwd( ), 'api_token.txt' ) )

if os.path.exists( _API_TOKEN_FILEPATH ):
	with open( _API_TOKEN_FILEPATH, 'r' ) as file:
		_API_TOKEN = file.readline( ).rstrip( )

_URL = 'https://api.race-monitor.com/v2/Common/AppSections --data "apiToken={0}"'.format( _API_TOKEN )

x = urllib.request.urlopen( _URL )
print( x.read( ) )
