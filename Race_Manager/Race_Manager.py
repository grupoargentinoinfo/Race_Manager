# -*- coding: utf-8 -*- 

"""
The requests module is used for HTTP communications with the Race Monitor API.
PIP can be used to install requests if it is needed for development. "pip install requests"

wxPython 3.x is used for the windowing toolkit. QT was considered but there is no version of
PySide 1.2x for Python 3.5 and PySide 2.x is, as of November 2016, not ready for production use.
The wxPython 3.x binary builds can be found here, https://wxpython.org/Phoenix/snapshot-builds/

**Author:**

	Jeff Hanna, 11/22/2016
"""

import wx

import core
import ui


def main( ) -> None:
	app = wx.App( )
	frame = ui.Main_Frame( )
	frame.Show( )
	app.MainLoop( )
	


if __name__ == '__main__':
	main( )