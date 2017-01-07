import datetime
import gettext
import wx
import wx.lib.agw.aui

import const
import core

_ = gettext.gettext


class Main_Panel( wx.Panel ):
	"""
	AUI Docking Pane managed panel that resides in Main_Frame under the ribbon
	"""

	def __init__( self, parent ):
		super( Main_Panel, self ).__init__( parent, wx.ID_ANY, style = wx.BORDER_NONE )
		
		self.SetDoubleBuffered( True )
		self.aui_mgr = wx.lib.agw.aui.AuiManager( )
		self.aui_mgr.SetManagedWindow( self )		
		
		self.lbx_competitors = wx.ListCtrl( self, wx.ID_ANY, style = wx.LC_LIST )#  | wx.LC_SORT_ASCENDING )
		self.aui_mgr.AddPane( self.lbx_competitors, 
								  wx.lib.agw.aui.AuiPaneInfo( ).
								  Name( 'lbx_competitors' ).
								  Left( ).
								  Caption( _( 'Competitors' ) ).
								  PinButton( True ).
								  Dock( ).
								  Resizable( ).
								  FloatingSize( self.lbx_competitors.GetSize( ) ).
								  DockFixed( False ).
								  Layer( 2 ) )
		
		self.nb_competitors = wx.lib.agw.aui.AuiNotebook( self, wx.ID_ANY, style = wx.lib.agw.aui.AUI_NB_DEFAULT_STYLE )
		self.aui_mgr.AddPane( self.nb_competitors, 
								  wx.lib.agw.aui.AuiPaneInfo( ).
								  Name( 'nb_live_data' ).
								  Center( ).
								  CaptionVisible( False ).
								  PinButton( True ).
								  Movable( False ).
								  Dock( ).
								  Resizable( ).
								  FloatingSize( wx.DefaultSize ).
								  BottomDockable( False ).
								  TopDockable( False ).
								  LeftDockable( False ).
								  RightDockable( False ).
								  Floatable( False ).
								  CentrePane( ).
								  DefaultPane( ) )
		
		self.Stopwatch_Panel = Stopwatch_Panel( self )
		self.aui_mgr.AddPane( self.Stopwatch_Panel, 
								  wx.lib.agw.aui.AuiPaneInfo( ).
								  Name( 'Stopwatch' ).
								  Bottom( ).
								  Caption( _('Stopwatch') ).
								  PinButton( True ).
								  Dock( ).
								  Resizable( ).
								  LeftDockable( False ).
								  RightDockable( False ).
								  FloatingSize( wx.Size( 42, 59 ) ).
								  DockFixed( False ).Layer( 1 ) )
		
		self.Clock_Panel = Clock_Panel( self )
		self.aui_mgr.AddPane( self.Clock_Panel, 
								  wx.lib.agw.aui.AuiPaneInfo( ).
								  Name( 'Clock_Panel' ).
								  Bottom( ).
								  Caption( _( 'Clock' ) ).
								  PinButton( True ).
								  Dock( ).
								  Resizable( ).
								  LeftDockable( False ).
								  RightDockable( False ).
								  FloatingSize( wx.Size( 42, 59 ) ).
								  DockFixed( False ).
								  Layer( 1 ) )		
		
		self.aui_mgr.Update( )
		self.Bind( wx.EVT_CLOSE, self.Close )

														 
	def __del__( self ):
		"""
		Required. If this wx.Frame is deleted without the AUI Manager being uninitialized an exception will be raised.
		"""

		self.aui_mgr.UnInit( )


	def Close( self, event ):
		"""
		Override of the standard Close( ) event with a call to uninitialize the AUI Manager
		"""

		self.__del__( )
		event.Skip( )


	def list_competitors( self, race_data ):
		"""
		1/6/2017
		"""

		self.lbx_competitors.ClearAll( )
		self.lbx_competitors.InsertColumn( 0, '' )
		if isinstance( race_data, core.Race_Data ):
			for i in range( len( race_data.competitor_numbers ) ):
				self.lbx_competitors.InsertItem( i, race_data.competitor_numbers[ i ] )



class Stopwatch_Panel( wx.Panel ):
	"""
	1/5/2017
	TODO: Set enable/disable states on buttons based on current state.
	"""

	def __init__(self, parent ):
		super( Stopwatch_Panel, self ).__init__( parent, wx.ID_ANY, style = wx.BORDER_NONE )

		szr_main = wx.BoxSizer( wx.VERTICAL )
		
		self.display = wx.StaticText( self, wx.ID_ANY, const.STOPWATCH_DEFAULT_VALUE, style = wx.ALIGN_CENTRE )
		self.display.Wrap( -1 )
		self.display.SetFont( wx.Font( 36, 70, 90, 90, False, 'Consolas' ) )
		
		szr_main.Add( self.display, 1, wx.ALIGN_CENTER, 0 )

		szr_buttons = wx.BoxSizer( wx.HORIZONTAL )
		self.btn_start_stop = wx.Button( self, wx.ID_ANY, _( 'Start / Stop' ) )
		self.btn_start_stop.Bind( wx.EVT_BUTTON, self._on_start_stop )
		szr_buttons.Add( self.btn_start_stop, 1, wx.EXPAND )
		self.btn_reset = wx.Button( self, wx.ID_ANY, _( 'Reset' ) )
		self.btn_reset.Bind( wx.EVT_BUTTON, self._on_reset )
		szr_buttons.Add( self.btn_reset, 1, wx.EXPAND )
		szr_main.Add( szr_buttons, 0, wx.EXPAND )

		self.timer = wx.Timer( self, wx.ID_ANY )
		self.stopwatch = wx.StopWatch( )
		
		self.Bind( wx.EVT_TIMER, self._on_timer )
		self.SetSizer( szr_main )

		self.stopwatch_start_value = 0 
														 
		
	def _on_start_stop( self, _event ):
		"""
		1/5/2017
		"""
	
		if not self.timer.IsRunning( ):
			self.stopwatch.Start( self.stopwatch_start_value )
			self.timer.Start( 10 )
		else:
			self.stopwatch.Pause( )
			self.timer.Stop( )
			self.stopwatch_start_value = self.stopwatch.Time( )
						

	def _on_reset( self, _event ):
		"""
		1/5/2017
		"""
		if self.timer.IsRunning( ):
			self.stopwatch.Pause( )
			self.timer.Stop( )
			wx.CallAfter( self._restart_stopwatch )

		self.display.SetLabel( const.STOPWATCH_DEFAULT_VALUE )


	def _restart_stopwatch( self ):
		"""
		1/6/2016
		"""

		self.stopwatch_current_value = 0
		self.stopwatch.Start( self.stopwatch_current_value )
		self.timer.Start( )


	def _on_timer( self, _event ):
		time = datetime.timedelta( milliseconds = self.stopwatch.Time( ) )
		val = str( time )[ :-3 ] # gives 6 digts of precision, trim to 3
		self.display.SetLabel( val )



class Clock_Panel( wx.Panel ):
	"""
	1/5/2017
	TODO: Support user selectable 12 and 24 hr time.
	TODO: Add support for alarm(s).
	"""

	def __init__( self, parent ):
		super( Clock_Panel, self ).__init__( parent, wx.ID_ANY, style = wx.BORDER_NONE )
		
		self.timer = wx.Timer( self, wx.ID_ANY )		
		self.timer.Start( 1000 ) 

		szr_main = wx.BoxSizer( wx.VERTICAL )
		
		self.display = wx.StaticText( self, wx.ID_ANY, '', style = wx.ALIGN_CENTRE )
		self.display.Wrap( -1 )
		self.display.SetFont( wx.Font( 36, 70, 90, 90, False, 'Consolas' ) )
		
		szr_main.Add( self.display, 1, wx.ALIGN_CENTER, 0 )

		self.Bind( wx.EVT_TIMER, self._on_timer )						
		self.SetSizer( szr_main )
		
		wx.CallAfter( self._on_timer, None )

				 		
	def _on_timer( self, _event ):
		time = datetime.datetime.now( ).time( )
		val = time.strftime( '%I:%M:%S %p' ).lstrip( '0' )
		self.display.SetLabel( val	)
