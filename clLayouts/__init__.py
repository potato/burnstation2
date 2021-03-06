#!/usr/bin/env python
# -*- coding: utf-8 -*-

# ----------------------------------------------------------------------------
# pyjama - python jamendo audioplayer
# Copyright (c) 2008 Daniel Nögel
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 3 of the License.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------------

## @package clLayouts
# This module manages the different layouts for pyjama
# e.g. AlbumBrowser, AlbumLayout and ArtistLayout

import gtk
import time


## Handling the Layouts.
# You'll have to register your custon Layout
# here.
class Layouts():
    ## The Constructor
    def __init__(self, pyjama):
        self.__pyjama = pyjama
        ## Dictionary filled with layouts later
        self.layouts = {}
        ## Dictionary filled with the layouts' toolbars later
        self.toolbars = {}
        ## Holds the currently shown layout
        self.current_layout = None

        self.__pyjama.Events.add_event("show_layout")

    ## Registers a layout.
    # Each Layout needs a methode draw() and a subclass called ToolBar().
    # See \ref layout-draw and \ref layout-toolbar.
    # @param self Object Pointer
    # @param layout_name The name of the layout to register
    # @param layout_class The layout class to call when you want you Layout to be shown
    # @return None
    def register_layout(self, layout_name, layout_class):
        self.layouts[layout_name] = layout_class
        self.toolbars[layout_name] = layout_class.ToolBar(self.__pyjama)
        self.__pyjama.window.vbMainLayout.pack_start(self.toolbars[layout_name], False, True)        

    ## Show a layout
    # This methode is the central layout function.
    # When you've registered your layout, you can show it
    # calling this function.
    # @param self Object Pointer
    # @param layout The layout to show (as registered in register_layout() before)
    # @param data1 Optional - Data you want to pass to your layout's draw() methode
    # @param data2 Optional - Data you want to pass to your layout's draw() methode
    # @param data3 Optional - Data you want to pass to your layout's draw() methode
    # @param data4 Optional - Data you want to pass to your layout's draw() methode
    # @param fromhistory Optional bool - default is False - If set to True the page won't be
    # stored in hinstory
    # @param who_called Optional - for debugging perpose only - which methode called this?
    # @return None
    # @todo
    # - use *args or **kargs as params instead of data(n)
    def show_layout(self, layout, data1=None, data2=None, data3=None, data4=None, fromhistory=False, who_called=""):       
        if self.__pyjama.debug:
            print ("Called by: %s" % who_called)

        # hiding the last layout's toolbar
        if self.current_layout != None and layout != self.current_layout:
            self.toolbars[self.current_layout].hide()

        # Unset Layout Info
        self.__pyjama.window.LayoutInfo.set_text("")
        self.__pyjama.window.LayoutInfo.set_image(None)

        #
        # History
        #
        if self.__pyjama.historyCurrent != {} and fromhistory==False:
            self.__pyjama.historyBack.append(self.__pyjama.historyCurrent)
        if fromhistory == False:
            self.__pyjama.historyForward = []
        self.__pyjama.historyCurrent = {'layout':layout, 'data1':data1, 'data2':data2, 'data3':data3, 'data4':data4}
        self.__pyjama.window.toolbar.bHistoryForward.set_sensitive(len(self.__pyjama.historyForward)>0)
        self.__pyjama.window.toolbar.bHistoryBack.set_sensitive(len(self.__pyjama.historyBack)>0)

        #
        # insert Layout into scrolledwindow
        #        
        if self.current_layout != None:
            self.__pyjama.window.scrolledwindow.remove(self.__pyjama.window.scrolledwindow.child)
            # For non-scrollable widgets - no scrollbars for some reasons
            # self.__pyjama.window.scrolledwindow.add_with_viewport(self.layouts[layout])
        if isinstance(self.layouts[layout], gtk.Layout):
            self.__pyjama.window.scrolledwindow.add(self.layouts[layout])
        else:
            self.__pyjama.window.scrolledwindow.add_with_viewport(self.layouts[layout])
        # Setting Scrollbars
        self.__pyjama.window.scrolledwindow.set_vadjustment(gtk.Adjustment(value=0, lower=0, upper=0, step_incr=0, page_incr=0, page_size=0))

        self.current_layout = layout
        
        # showing the toolbar
        self.toolbars[layout].show()
        # calling the layout's draw method:,
        self.layouts[layout].draw(data1, data2, data3, data4)
        self.__pyjama.window.do_events()
