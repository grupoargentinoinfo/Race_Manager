# -*- coding: utf-8 -*- 

"""
Core logic for Race Manager.

The requests module is used for HTTP communications with the Race Monitor API.
PIP can be used to install requests if it is needed for development. 'pip 
install requests'

wxPython 3.x is used for the windowing toolkit. QT was considered but there is 
no version of PySide 1.2x for Python 3.5 and PySide 2.x is, as of November 2016,
not ready for production use. The wxPython 3.x binary builds can be found here, 
https://wxpython.org/Phoenix/snapshot-builds/

**Author:**

	Jeff Hanna, 11/22/2016
"""

import json
import os
import requests
import time

import const


class Race_Data( object ):
	"""
	"""

	def __init__( self, race_info ):
		self._name = race_info.get( const.API_RACE_NAME_KEY)
		self._race_id = race_info.get( const.API_ID_KEY )
		self._session = { }

	@property
	def name( self ):
		return self._name		 

	@property
	def race_id( self ):
		return self._race_id

	@property 
	def session( self ):
		return self._session

	@session.setter
	def session( self, data ):
		self._session = data

	@property
	def session_name( self ):
		return self._session.get( const.API_RACE_NAME_KEY, '' )
	
	@property
	def session_date( self ):
		return self._session.get( 'SessionDate', '' )

	@property
	def session_time( self ):
		return self._session.get( 'SessionTime', '' )
	
	@property
	def competitors( self ):
		return self._competitors

	@property
	def competitor_names( self ):
		return [ ]

	@property
	def competitor_numbers( self ):
		sorted_competitors = self._session.get( 'SortedCompetitors', [ ] )
		if sorted_competitors:
			numbers = [ x.get( 'Number', -1 ) for x in sorted_competitors ]
			numbers.sort( )
			return numbers



def __get_api_token( ):
	"""
	Gets the Race Monitor issued api token for this application.
	The api token is stored in an external file named 'api_token.txt'. That file 
	is not sync'd to the GIT repository so that the token remains secure.
	
	TODO:
	This will have to be replaced with a secure internal token storage system 
	if/when the software gets published commercially.
	"""

	if os.path.exists( const.__API_TOKEN_FILEPATH ):
		with open( const.__API_TOKEN_FILEPATH, 'r' ) as file:
			api_token = file.readline( ).rstrip( )

	return api_token or ''


def __local_query( url_path, pdata = { } ):
	"""
	# USE LOCAL DATA, IF IT EXISTS, TO GET AROUND API RATE LIMIT WHILE DEVELOPING
	# TODO: REMOVE IN PRODUCTION BUILDS
	"""

	filename = ''
	for id in [ const.API_RACE_ID_KEY, const.API_SESSION_ID_KEY, const.API_RACE_ID_KEY, const.API_SERIES_ID_KEY ]:
		id_val = pdata.get( id, '' )
		if id_val:
			filename = '{0}_{1}.json'.format( url_path.replace( '/', '_' ), id_val )

	if not filename:
		filename = '{0}.json'.format( url_path.replace( '/', '_' ) )

	filepath = os.path.join( os.getcwd( ), 'json_data', filename )
	if os.path.exists( filepath ):
		with open( filepath, 'r' ) as file:
			data = json.load( file )
	else:
		# Fallback to actual web API if the local data doesn't exist.
		time.sleep( 45 )
		data = __query_race_monitor( url_path, pdata, override_use_local = True )
		success = data.get( const.API_SUCCESSFUL_KEY, False )
		
		if success:	 		 		
			if not filename:
				filename = '{0}.json'.format( url_path.replace( '/', '_' ) )

			filepath = os.path.join( os.getcwd( ), 'json_data', filename )
			with open( filepath, 'w') as file:
				json.dump( data, file )

	return data
					  

def __query_race_monitor( url_path, post_data = { }, override_use_local = False ):
	"""
	"""

	url = const.RACE_MONITOR_URL + url_path
	__api_token = __get_api_token( )

	if __api_token:
		pdata = { const.API_TOKEN_KEY : __api_token }
		pdata.update( post_data )		
		
		# USE LOCAL DATA, IF IT EXISTS, TO GET AROUND API RATE LIMIT WHILE DEVELOPING
		# TODO: REMOVE IN PRODUCTION BUILDS
		if const.USE_LOCAL_DATA and not override_use_local:
			data = __local_query( url_path, pdata )
		else:
			data = requests.post( url, pdata ).json( )
		
		success = data.get( const.API_SUCCESSFUL_KEY, False )
		if success:
			return data
		else:
			# TODO: Handle various failure cases as outlined in the Race Monitor 
			# API docs
			message = data.get( const.API_MESSAGE_KEY, '' )
			raise Exception( message )
	

def get_app_sections( ):
	"""
	"""

	data = __query_race_monitor( 'Common/AppSections' )

	if data:
		app_sections = data.get( const.API_APP_SECTIONS_KEY, [ ] )
		return app_sections

	return [ ]


def get_races( series_id ):
	"""
	# TODO: Switch from Common/PastRaces to Common/CurrentRaces when getting 
	# live timing. 
	"""
		
	data = __query_race_monitor( 'Common/PastRaces', post_data = { const.API_SERIES_ID_KEY : series_id } )

	if data:
		races = data.get( const.API_RACES_KEY, [ ] ) # list of dictionaries
		return races

	return [ ]


def get_race_data( race_info ):
	"""
	"""

	race_data = Race_Data( race_info )

	post_data = { const.API_RACE_ID_KEY : race_data.race_id }
	is_live = False

	# Check to see if the race is live.
	data = __query_race_monitor( 'Race/IsLive', post_data = post_data )

	if data:
		is_live = data.get( const.API_IS_LIVE_KEY, False )

	api_url = 'Live/GetSession' if is_live else 'Results/SessionDetails'	
	post_data = { const.API_SESSION_ID_KEY : race_data.race_id }

	data = __query_race_monitor( api_url, post_data = post_data )
	
	if data:
		race_data.session = data.get( const.API_SESSION_KEY, { } )

	#else:
		#raise Exception( 'Could not retrieve session data.' )	 

	return race_data
