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

		self.aui_mgr = wx.lib.agw.aui.AuiManager( )
		self.aui_mgr.SetManagedWindow( self )		
		self.aui_mgr.AddPane( self._create_main_pane( ), wx.lib.agw.aui.AuiPaneInfo( ).Name( _( "Main" ) ).CenterPane( ) )
					
		self.aui_mgr.Update( )
		self.Bind( wx.EVT_CLOSE, self.Close )


	def _create_main_pane( self : wx.Window ) -> wx.Panel:
		"""
		TODO: This needs to be a control, not a panel.
		"""

		pnl = wx.Panel( self, wx.ID_ANY, style = wx.BORDER_NONE ) 		
		return pnl

		

	def __del__( self : wx.Window ) -> None:
		"""
		Required. If this wx.Frame is deleted without the AUI Manager being uninitialized an exception will be raised.
		"""

		self.aui_mgr.UnInit( )


	def Close( self : wx.Window, event : wx.Event ) -> None:
		"""
		Override of the standard Close( ) event with a call to uninitialize the AUI Manager
		"""

		self.__del__( )
		event.Skip( )