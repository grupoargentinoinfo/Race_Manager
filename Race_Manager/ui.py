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

		

class Race_Selection_Dialog( wx.Dialog ):
	def __init__( self, parent : wx.Window, app_sections : dict ) -> None:
		super( Race_Selection_Dialog, self ).__init__( parent,
																	id = wx.ID_ANY,
																	title = const.RACE_SELECTION_DLG_TITLE,
																	pos = const.RACE_SELECTION_DLG_DEFAULT_POSITION,
																	size = const.RACE_SELECTION_DLG_DEFAULT_SIZE,
																 )

		self._race_data = None 
		self._app_sections = app_sections
	
		app_section_names = [ x.get( const.API_NAME_KEY ).lstrip( ) for x in self._app_sections if 
									 x.get( const.API_NAME_KEY ) not in const.NAME_IGNORE_LIST ]
		
		sizer = wx.BoxSizer( wx.VERTICAL )
		self.lbx_app_sections = wx.ListBox( self, 
														wx.ID_ANY, 
														wx.DefaultPosition, 
														wx.DefaultSize,
														app_section_names, 
														style = wx.LB_SINGLE | wx.LB_SORT )

		sizer.Add( self.lbx_app_sections, 0, wx.ALL | wx.EXPAND, 3 )
		self.lbx_app_sections.Bind( wx.EVT_LISTBOX, self._on_listbox )
		self.lbx_app_sections.Bind( wx.EVT_LISTBOX_DCLICK, self._on_listbox_dclick )

		btn_sizer = wx.Dialog.CreateSeparatedButtonSizer( self, wx.OK | wx.CANCEL )
		sizer.Add( btn_sizer, 0, wx.ALL | wx.EXPAND, 3 )

		self.SetSizer( sizer )
		self.Centre( wx.BOTH )


	@property
	def race_data( self: wx.Window ) -> dict:
		return self._race_data
	
	
	def _on_listbox( self, event : wx.Event ) -> None:
		ctrl = event.GetEventObject( )
		name = ctrl.GetStringSelection( )
		for x in self._app_sections:
			if x.get( const.API_NAME_KEY, '').lstrip( ) == name: # Dirt Oval and Paved Oval have leading spaces.
				self._race_data = x
				return( )

	
	def _on_listbox_dclick( self, event : wx.Event ) -> None:
		self.EndModal( wx.ID_OK )
