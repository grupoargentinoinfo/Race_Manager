"""
wx Python based UI elements for Race Monitor

**Author:**

	Jeff Hanna, 11/24/2016
"""

import os
import wx

import const
import core

class Main_Frame( wx.Frame ):
	def __init__( self ) -> None:
		self._race_data = { }

		super( Main_Frame, self ).__init__( parent = None,
														 id = wx.ID_ANY,
														 title = const.MAIN_FRAME_TITLE,
														 pos = const.MAIN_FRAME_DEFAULT_POSITION,
														 size = const.MAIN_FRAME_DEFAULT_SIZE, 
													  )

		sizer = wx.BoxSizer( wx.VERTICAL )
		self.SetSizer( sizer )
		self.Layout( )
		self.Centre( wx.BOTH )
		
		wx.CallAfter( self._get_current_race )
		
	
	def _get_current_race( self : wx.Window ):
		if os.path.exists( const.PREFS_FILEPATH ):
			# TODO: Put in code to detect a previously selected section/race.
			# If that race is still ongoing (based on date/time) reload it.
			# Otherwise, ask the user to pick a section/race.
			pass
		else:
			app_sections = core.get_app_sections( )
			dlg = Race_Selection_Dialog( self, app_sections )
			if dlg.ShowModal( ) == wx.ID_OK:
				self._race_data = dlg.race_data
				wx.MessageBox( self._race_data.get( const.API_NAME_KEY, '' ) )

			dlg.Destroy( )

		

class Race_Selection_Dialog ( wx.Dialog ):
	def __init__( self, parent : wx.Window, app_sections : dict ) -> None:
		super( Race_Selection_Dialog, self ).__init__( parent,
																	  id = wx.ID_ANY,
																	  title = const.RACE_SELECTION_DLG_TITLE,
																	  pos = const.RACE_SELECTION_DLG_DEFAULT_POSITION,
																	  size = const.RACE_SELECTION_DLG_DEFAULT_SIZE,
																	  style = wx.DEFAULT_DIALOG_STYLE, )
							
		self._app_sections = app_sections
		self._race_data = None
		
		sizer = wx.BoxSizer( wx.VERTICAL ) 	
			
		self.lbk_races = wx.Listbook( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, wx.LB_DEFAULT )			
		sizer.Add( self.lbk_races, 1, wx.EXPAND | wx.ALL, 3 )

		btn_sizer = wx.Dialog.CreateStdDialogButtonSizer( self, wx.OK | wx.CANCEL )
		sizer.Add( btn_sizer, 0, wx.EXPAND | wx.ALL, 3 )  
		
		self._add_app_section_pages( )
		
		self.SetSizer( sizer )
		self.Layout( )	 		
		self.Centre( wx.BOTH )


	@property
	def race_data( self : wx.Window ) -> dict:
		return self._race_data


	def _add_app_section_pages( self : wx.Window ) -> None:
		for x in self._app_sections:
			name = x.get( const.API_NAME_KEY, '' ).lstrip( ) # Oval race types have leading spaces for list identation, remove them.
			if name not in const.NAME_IGNORE_LIST:
				page = Race_List_Panel_Base( self.lbk_races, x )
				self.lbk_races.AddPage( page, page.name )



class Race_List_Panel_Base ( wx.Panel ):
	def __init__( self, parent : wx.Window, app_section: dict ) -> None:
		super( Race_List_Panel_Base, self ).__init__( parent,
																	 id = wx.ID_ANY,
																	 pos = wx.DefaultPosition,
																	 size = wx.DefaultSize, 
																	 style = wx.TAB_TRAVERSAL, )

		self._app_section = app_section
		self._series_id = self._app_section.get( const.API_ID_KEY, 0 )
		self._current_races = core.get_current_races( self._series_id )
		self._past_races = core.get_past_races( self._series_id )
		
		sizer = wx.BoxSizer( wx.VERTICAL )
		
		race_names = [ x.get( const.API_NAME_KEY, '' ) for x in self._current_races ]	
		race_names.extend( [ x.get( const.API_NAME_KEY, '' ) for x in self._past_races ] )
					
		self.lbx_races = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, race_names, style = wx.LB_SORT )
		sizer.Add( self.lbx_races, 1, wx.ALL|wx.EXPAND, 3 )
		
		self.SetSizer( sizer )


	@property
	def name( self : wx.Panel ) -> str:
		return self._app_section.get( const.API_NAME_KEY, '' ).lstrip( ) # oval race types have leading spaces in the names.
	

	@property
	def image_name( self : wx.Panel ) -> str:
		return self._app_section.get( const.API_IMAGES_KEY, '' )[ 0 ]


	@property
	def id( self : wx.Panel ) -> int:
		return self._series_id