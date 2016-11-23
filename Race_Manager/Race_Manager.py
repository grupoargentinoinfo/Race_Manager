"""
Race stratgy manager that utilizes Race Monitor data streams.

**Author:**

	Jeff Hanna, 11/22/2016
"""

import io
import os
import pycurl
import urllib.request
import requests


_API_TOKEN_FILEPATH = os.path.abspath( os.path.join( os.getcwd( ), 'api_token.txt' ) )

if os.path.exists( _API_TOKEN_FILEPATH ):
	with open( _API_TOKEN_FILEPATH, 'r' ) as file:
		_API_TOKEN = file.readline( ).rstrip( )

_URL = 'https://api.race-monitor.com/v2/Common/AppSections --data "apiToken={0}"'.format( _API_TOKEN )


def use_pycurl( url ):
	"""
	Attempt to use PyCurl to utilize the URL to get the race data.
	CUrrently it fails with an 'HTTP Error 400: Bad Request occurred'.
	Note: Setting pycurl.SSL)VERIFYPEER and pycurl.SSL_VERIFYHOST to 0 
	and not setting a certificate path for pycurl.CAINFO is BAD. It makes
	the program completely vulnerable to man in the middle attacks.
	DO NOT USE IN PRODUCTION WITH THE SSL OPTIONS DISABLED>

	**Arguments:**
		
		:``url``: `string` The race monitor URL with api token

	**Keyword Arguments:**

		None

	**Todo:**

		Properly set up SSL protections before using in production.

	**Author:**

		Jeff Hanna, 11/22/2016
	"""

	buffer = io.BytesIO( )
	c = pycurl.Curl( )
	c.setopt( pycurl.URL, url )
	c.setopt( pycurl.SSL_VERIFYPEER, 0 ) #1
	c.setopt( pycurl.SSL_VERIFYHOST, 0 ) #2
	#c.setopt( pycurl.CAINFO, '' )
	c.setopt( pycurl.WRITEDATA, buffer )
	c.perform( )
	c.close( )

	body = buffer.getvalue( )
	print( body.decode( 'iso-8859-1' ) )


def use_requests( url ):
	"""
	Attempt to use urllib to utilize the URL to get the race data.
	CUrrently it returns text saying the data requested couldn't be found.
	This is the same return text as if the URL was pasted into a web browser's
	address bar and entered.

	**Arguments:**
		
		:``url``: `string` The race monitor URL with api token

	**Keyword Arguments:**

		None

	**Author:**

		Jeff Hanna, 11/22/2016
	"""

	body = requests.get( url )
	print( body.text )



def use_urllib( url ):
	"""
	Attempt to use urllib to utilize the URL to get the race data.
	CUrrently it fails with an 'HTTP Error 400: Bad Request occurred'.

	**Arguments:**
		
		:``url``: `string` The race monitor URL with api token

	**Keyword Arguments:**

		None

	**Author:**

		Jeff Hanna, 11/22/2016
	"""

	body = urllib.request.urlopen( url )
	print( body.read( ) )


if __name__ == '__main__':
	#use_pycurl( _URL )
	use_requests( _URL )
	#use_urllib( _URL )
