# -*- coding: utf-8 -*- 

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


def __get_api_token( ) -> str:
	"""
	Gets the Race Monitor issued api token for this application.
	The api token is stored in an external file named 'api_token.txt'. That file is not
	sync'd to the GIT repository so that the token remains secure.
	
	TODO:
	This will have to be replaced with a secure internal token storage system if/when the
	software gets published commercially.
	"""

	if os.path.exists( const.__API_TOKEN_FILEPATH ):
		with open( const.__API_TOKEN_FILEPATH, 'r' ) as file:
			api_token = file.readline( ).rstrip( )

	return api_token or ''


def __query_race_monitor( url_path : str, post_data : dict = { } ) -> dict :
	url = const.RACE_MONITOR_URL + url_path
	__api_token = __get_api_token( )

	if __api_token:
		pdata = { const.API_TOKEN_KEY : __api_token }
		pdata.update( post_data )

		data = requests.post( url, pdata ).json( )
		
		success = data.get( const.API_SUCCESSFUL_KEY, False )
		if success:
			return data
		else:
			# TODO: Handle various failure cases as outlined in the Race Monitor API docs
			message = data.get( const.API_MESSAGE_KEY, '' )
			raise Exception( message )
	

def get_app_sections( ) -> list:
	data = __query_race_monitor( 'Common/AppSections' )

	if data:
		app_sections = data.get( const.API_APP_SECTIONS_KEY, [ ] )
		return app_sections

	return [ ]


def get_races( series_id : int ) -> list:
	# TODO: Switch from Common/PastRaces to Common/CurrentRaces when getting live timing. 
	data = __query_race_monitor( 'Common/PastRaces', #CurrentRaces', 
										  post_data = { const.API_SERIES_ID_KEY : series_id } )

	if data:
		races = data.get( const.API_RACES_KEY, [ ] ) # list of dictionaries
		return races

	return [ ]


def get_race_data( race_id : int ) -> tuple:
	# TODO: CONSULT WITH RACE-MONITOR DEVS ABOUT CORRECT USAGE OF API TO GET THIS DATA.
	# TODO: Make return data a class instead of a tuple of dicts?
	post_data = { const.API_RACE_ID_KEY : race_id }
	is_live = False

	# Check to see if the race is live.
	data = __query_race_monitor( 'Race/IsLive',
										   post_data = post_data )

	if data:
		is_live = data.get( const.API_IS_LIVE_KEY, False )

	if is_live:
		data = __query_race_monitor( 'Live/GetSession', 
											  post_data = post_data )
	
		if data:
			session = data.get( const.API_SESSION_KEY, { } )
			competitors = data.get( const.API_COMPETITORS_KEY, { } )
			return ( session, competitors )

		return ( )

	else:
		raise Exception( 'Race is not live' )
