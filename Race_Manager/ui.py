# -*- coding: utf-8 -*- 

"""
wx Python based UI elements for Race Monitor

**Author:**

	Jeff Hanna, 11/24/2016
"""

import os
import wx
import wx.lib.agw.labelbook
import wx.lib.agw.aui
import wx.lib.agw.ribbon as rb

import const
import core
import gettext
_ = gettext.gettext


class Main_Frame( wx.Frame ):
	def __init__( self ) -> None:
		self._race_data = { }

		super( Main_Frame, self ).__init__( parent = None,
														id = wx.ID_ANY,
														title = const.MAIN_FRAME_TITLE,
														pos = const.MAIN_FRAME_DEFAULT_POSITION,
														size = const.MAIN_FRAME_DEFAULT_SIZE, )
				
		self.aui_mgr = wx.lib.agw.aui.AuiManager( )
		self.aui_mgr.SetManagedWindow( self )
		self.aui_mgr.SetAGWFlags( wx.lib.agw.aui.AUI_MGR_DEFAULT )
		
		self.ribbon_bar = rb.RibbonBar( self, 
												  wx.ID_ANY, 
												  wx.DefaultPosition, 
												  wx.DefaultSize, 
												  wx.lib.agw.ribbon.RIBBON_BAR_DEFAULT_STYLE | wx.lib.agw.ribbon.RIBBON_BAR_SHOW_PAGE_LABELS )

		self.aui_mgr.AddPane( self.ribbon_bar, 
									 wx.lib.agw.aui.AuiPaneInfo( ).
									 Top( ).
									 CaptionVisible( False ).
									 CloseButton( False ).
									 PaneBorder( False ).
									 Dock( ).
									 Resizable( ).
									 FloatingSize( wx.DefaultSize ).
									 DockFixed( True ).
									 BottomDockable( False ).
									 LeftDockable( False ).
									 RightDockable( False ).
									 Floatable( False ) )
		
		self.ribbon_page_file = rb.RibbonPage( self.ribbon_bar, 
															wx.ID_ANY, 
															_( "File" ), 
															wx.NullBitmap,
															0 )
		self.ribbon_bar.SetActivePage( self.ribbon_page_file ) 

		self.ribbon_panel_file = rb.RibbonPanel( self.ribbon_page_file, 
															  wx.ID_ANY, 
															  wx.EmptyString, 
															  wx.NullBitmap, 
															  wx.DefaultPosition, 
															  wx.DefaultSize, 
															  wx.lib.agw.ribbon.RIBBON_PANEL_DEFAULT_STYLE )
		
		self.ribbon_button_bar_file = rb.RibbonButtonBar( self.ribbon_panel_file, 
																		  wx.ID_ANY, 
																		  wx.DefaultPosition, 
																		  wx.DefaultSize, 
																		  0 )
		
		self.ribbon_button_bar_file.AddSimpleButton( wx.ID_ANY, 
																	_( "Pick Race" ), 
																	wx.ArtProvider.GetBitmap( wx.ART_QUESTION, wx.ART_OTHER, wx.Size( 32, 32 ) ),
																	wx.EmptyString )
		
		self.ribbon_page_current_race = rb.RibbonPage( self.ribbon_bar, 
																	  wx.ID_ANY, 
																	  _( "Current Race" ), 
																	  wx.NullBitmap, 
																	  0 )
		#self.ribbon_bar.Realize( )
		
		self.status_bar = self.CreateStatusBar( 1, wx.STB_SIZEGRIP, wx.ID_ANY )
		
		self.aui_mgr.Update( )
		self.Centre( wx.BOTH )
		
		self.Bind( wx.EVT_CLOSE, self.Close )
		wx.CallAfter( self._get_current_race )

	
	def __del__( self: wx.Window ):
		self.aui_mgr.UnInit( )
																  																  		
	
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
				wx.MessageBox( self._race_data[ 0 ].get( const.API_NAME_KEY, '' ) )

			dlg.Destroy( )

	
	def Close( self : wx.Window, event : wx.Event ):
		self.__del__( )
		event.Skip( )



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
			
		self.lbk_races = wx.lib.agw.labelbook.LabelBook( self, 
																		 wx.ID_ANY, 
																		 wx.DefaultPosition, 
																		 wx.DefaultSize, 
																		 agwStyle = wx.lib.agw.labelbook.INB_FIT_LABELTEXT | 
																						wx.lib.agw.labelbook.INB_BOLD_TAB_SELECTION | 
																						wx.lib.agw.labelbook.INB_SHOW_ONLY_TEXT )	

		self.lbk_races.Bind( wx.lib.agw.labelbook.EVT_IMAGENOTEBOOK_PAGE_CHANGING, self._on_listbook_page_changing )		
		sizer.Add( self.lbk_races, 1, wx.EXPAND | wx.ALL, 3 )

		btn_sizer = wx.Dialog.CreateStdDialogButtonSizer( self, wx.OK | wx.CANCEL )
		sizer.Add( btn_sizer, 0, wx.EXPAND | wx.ALL, 3 )  
		
		self._add_app_section_pages( )
		
		self.SetSizer( sizer )
		self.Layout( )	 		
		self.Centre( wx.BOTH )
						
		wx.CallAfter( self._list_races_on_first_page ) 


	@property
	def race_data( self : wx.Window ) -> dict:
		return self._race_data


	def _add_app_section_pages( self : wx.Window ) -> None:
		for x in self._app_sections:
			name = x.get( const.API_NAME_KEY, '' ).lstrip( ) # Oval race types have leading spaces for list identation, remove them.
			if name not in const.NAME_IGNORE_LIST:
				page = Race_List_Panel_Base( self.lbk_races, x, self._get_race_name_callback )
				self.lbk_races.AddPage( page, page.name )


	def _list_races_on_first_page( self : wx.Window ) -> None:
		page = self.lbk_races.GetPage( 0 )
		page.list_races( )

		
	def _on_listbook_page_changing( self : wx.Window, event : wx.Event ) -> None:
		page_idx = event.GetSelection( )
		page = self.lbk_races.GetPage( page_idx )
		page.list_races( )


	def _get_race_name_callback( self : wx.Dialog, race_data : dict, end_modal : bool = False ) -> None:
		self._race_data = race_data
		if end_modal:
			self.EndModal( wx.ID_OK )


	
class Race_List_Panel_Base ( wx.Panel ):
	def __init__( self, parent : wx.Window, app_section: dict, selection_callback  ) -> None:
		super( Race_List_Panel_Base, self ).__init__( parent,
																	 id = wx.ID_ANY,
																	 pos = wx.DefaultPosition,
																	 size = wx.DefaultSize, 
																	 style = wx.TAB_TRAVERSAL, )

		self._app_section = app_section
		self._selection_callback = selection_callback

		self._series_id = self._app_section.get( const.API_ID_KEY, 0 )
		self._races = [ ]
		self._race_names = [ ]
		
		sizer = wx.BoxSizer( wx.VERTICAL )
		
		self.lbx_races = wx.ListBox( self, wx.ID_ANY, wx.DefaultPosition, wx.DefaultSize, self._race_names, style = wx.LB_SORT )
		self.lbx_races.Bind( wx.EVT_LISTBOX, self._on_listbox )
		self.lbx_races.Bind( wx.EVT_LISTBOX_DCLICK, self._on_listbox_dclick )

		sizer.Add( self.lbx_races, 1, wx.ALL | wx.EXPAND, 3 )
		
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


	def _on_listbox( self : wx.Panel, event : wx.Event ) -> None:
		ctrl = event.GetEventObject( )
		selection = ctrl.GetSelection( )
		race_name = ctrl.GetString( selection )
		
		for x in self._races:
			if x.get( const.API_NAME_KEY, '' ) == race_name:
				race_id = x.get( const.API_ID_KEY, -1 )
				if race_id >= 0:
					race_data = core.get_race_data( race_id )
					self._selection_callback( race_data )
					break


	def _on_listbox_dclick( self : wx.Panel, event : wx.Event ) -> None:
		ctrl = event.GetEventObject( )
		selection = ctrl.GetSelection( )
		race_name = ctrl.GetString( selection )
		
		for x in self._races:
			if x.get( const.API_NAME_KEY, '' ) == race_name:
				race_id = x.get( const.API_ID_KEY, -1 )
				if race_id >= 0:
					race_data = core.get_race_data( race_id )
					self._selection_callback( race_data, end_modal = True )
					break

												 		
	def list_races( self : wx.Panel ) -> None:
		if not self._race_names:
			if not self._races:
				self._races = core.get_races( self._series_id )
			self._race_names = [ x.get( const.API_NAME_KEY, '' ) for x in self._races ]	
			self.lbx_races.Set( self._race_names )
