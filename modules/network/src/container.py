#!/usr/bin/env python
#-*- coding:utf-8 -*-


from theme import app_theme
from dtk.ui.button import  ToggleButton
#from dtk.ui.draw import draw_pixbuf, draw_text
#from dtk.ui.constant import DEFAULT_FONT_SIZE
import gtk

ICON_PADDING = 5
TEXT_PADDING = 5
BUTTON_PADDING = 5
class Contain(gtk.Alignment):

    def __init__(self, icon, text, switch_callback= None):

        gtk.Alignment.__init__(self, 0,0,0,0)

        self.icon = icon
        self.text = text
        self.show()
        self.active_cb = switch_callback
        self.hbox = gtk.HBox()
        self.add(self.hbox)

        self.image = gtk.Image()
        self.height = app_theme.get_pixbuf("/Network/switch_off.png").get_pixbuf().get_height()
        self.width = app_theme.get_pixbuf("/Network/switch_off.png").get_pixbuf().get_width()
        self.image.set_from_pixbuf(icon.get_pixbuf())
        self.hbox.pack_start(self.image, False, False, ICON_PADDING)
        self.label = gtk.Label(text)
        self.hbox.pack_start(self.label, False, False, TEXT_PADDING)

        self.switch = ToggleButton(
                app_theme.get_pixbuf("/Network/switch_off.png"), 
                app_theme.get_pixbuf("/Network/switch_on.png"))

        self.switch.connect("toggled", self.active_cb)
        self.hbox.pack_start(self.switch)
    
    def set_active(self, state):
        self.switch.set_active(state)

if __name__=="__main__":
    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_title("Container")
    #win.border_width(2)

    win.connect("destroy", lambda w: gtk.main_quit())
    
    con = Contain(app_theme.get_pixbuf("/Network/wired.png"), "有线网络", lambda w : "sfdsf")

    vbox = gtk.VBox(False)
    vbox.pack_start(con)
    win.add(vbox)
    win.show_all()

    gtk.main()