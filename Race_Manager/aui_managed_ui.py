import gettext
import wx
import wx.lib.agw.aui

_ = gettext.gettext


class Main_Panel( wx.Panel ):
	"""
	AUI Docking Pane managed panel that resides in Main_Frame under the ribbon
	"""

	def __init__( self : wx.Window , parent : wx.Window ) -> None:
		super( Main_Panel, self ).__init__( parent, wx.ID_ANY, style = wx.BORDER_NONE )

		self.m_mgr = wx.lib.agw.aui.AuiManager( )
		self.m_mgr.SetManagedWindow( self )		
		
		self.lbx_competitors = wx.ListCtrl( self, wx.ID_ANY, style = wx.LC_ICON )
		self.m_mgr.AddPane( self.lbx_competitors, 
								  wx.lib.agw.aui.AuiPaneInfo( ).
								  Name( 'lbx_competitors' ).
								  Left( ).
								  Caption( _( 'Competitors' ) ).
								  PinButton( True ).
								  Dock( ).
								  Resizable( ).
								  FloatingSize( wx.Size( 112, 115 ) ).
								  DockFixed( False ).
								  Layer( 2 ) )
		
		self.nb_competitors = wx.lib.agw.aui.AuiNotebook( self, wx.ID_ANY, style = wx.lib.agw.aui.AUI_NB_DEFAULT_STYLE )
		self.m_mgr.AddPane( self.nb_competitors, 
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
		
		self.PLACEHOLDER = wx.Panel( self.nb_competitors, wx.ID_ANY, style = wx.TAB_TRAVERSAL )
				
		self.Stopwatch_Panel = Stopwatch_Panel( self )
		self.m_mgr.AddPane( self.Stopwatch_Panel, 
								  wx.lib.agw.aui.AuiPaneInfo( ).
								  Name( 'Stopwatch' ).
								  Top( ).
								  Caption( _('Stopwatch') ).
								  PinButton( True ).
								  Dock( ).
								  Resizable( ).
								  FloatingSize( wx.Size( 42, 59 ) ).
								  DockFixed( False ).Layer( 1 ) )
		
		self.Clock_Panel = Clock_Panel( self )
		self.m_mgr.AddPane( self.Clock_Panel, 
								  wx.lib.agw.aui.AuiPaneInfo( ).
								  Name( 'Clock_Panel' ).
								  Top( ).
								  Caption( _( 'Clock' ) ).
								  PinButton( True ).
								  Dock( ).
								  Resizable( ).
								  FloatingSize( wx.Size( 42, 59 ) ).
								  DockFixed( False ).
								  Layer( 1 ) )		
		
		self.m_mgr.Update( )
		self.Bind( wx.EVT_CLOSE, self.Close )

														 
	def __del__( self : wx.Window ) -> None:
		"""
		Required. If this wx.Frame is deleted without the AUI Manager being uninitialized an exception will be raised.
		"""

		self.m_mgr.UnInit( )


	def Close( self : wx.Window, event : wx.Event ) -> None:
		"""
		Override of the standard Close( ) event with a call to uninitialize the AUI Manager
		"""

		self.__del__( )
		event.Skip( )



class Stopwatch_Panel( wx.Panel ):
	"""
	1/5/2017
	"""

	def __init__(self, parent ):
		super( Stopwatch_Panel, self ).__init__( parent, wx.ID_ANY, style = wx.BORDER_NONE )
		szr_main = wx.BoxSizer( wx.VERTICAL )
		
		self.display = wx.StaticText( self, wx.ID_ANY, _( '00:00:00' ), style = wx.ALIGN_CENTRE )
		self.display.Wrap( -1 )
		self.display.SetFont( wx.Font( 48, 70, 90, 90, False, wx.EmptyString ) )
		
		szr_main.Add( self.display, 1, wx.ALIGN_CENTER, 0 )

		szr_buttons = wx.BoxSizer( wx.HORIZONTAL )
		btn_start = wx.Button( self, wx.ID_ANY, _( 'Start' ) )
		szr_buttons.Add( btn_start, 1, wx.EXPAND )
		btn_pause = wx.Button( self, wx.ID_ANY, _( 'Pause' ) )
		szr_buttons.Add( btn_pause, 1, wx.EXPAND )
		btn_stop = wx.Button( self, wx.ID_ANY, _( 'Stop' ) )
		szr_buttons.Add( btn_stop, 1, wx.EXPAND )
		btn_reset = wx.Button( self, wx.ID_ANY, _( 'Reset' ) )
		szr_buttons.Add( btn_reset, 1, wx.EXPAND )
		szr_main.Add( szr_buttons, 0, wx.EXPAND )
		
		self.SetSizer( szr_main )
		self.Layout( )



class Clock_Panel( wx.Panel ):
	"""
	1/5/2017
	TODO: Support 12 and 24 hr time.
	"""

	def __init__(self, parent ):
		super( Clock_Panel, self ).__init__( parent, wx.ID_ANY, style = wx.BORDER_NONE )
		szr_main = wx.BoxSizer( wx.VERTICAL )
		
		self.display = wx.StaticText( self, wx.ID_ANY, _( '00:00 AM' ), style = wx.ALIGN_CENTRE )
		self.display.Wrap( -1 )
		self.display.SetFont( wx.Font( 48, 70, 90, 90, False, wx.EmptyString ) )
		
		szr_main.Add( self.display, 1, wx.ALIGN_CENTER, 0 )

		self.timer = wx.Timer( self, wx.ID_ANY )
					
		self.SetSizer( szr_main )
		self.Layout( )


