#!/usr/bin/env python
#-*- coding:utf-8 -*-
from theme import app_theme
from dtk.ui.button import ImageButton, ToggleButton
from dtk.ui.entry import Entry
from dtk.ui.theme import ui_theme
from dtk.ui.utils import color_hex_to_cairo, alpha_color_hex_to_cairo, cairo_disable_antialias, container_remove_all, is_single_click, is_double_click

import gtk
class CheckButtonM(ToggleButton):

    def __init__(self, group,connection ,callback,padding_x = 8):
        self.label = connection.get_setting("connection").id

        ToggleButton.__init__(self,
                              app_theme.get_pixbuf("Network/check_box_out.png"),
                              app_theme.get_pixbuf("Network/check_box.png"),
                              button_label = self.label, padding_x = padding_x)
        self.group_list = []
        self.leader = None
        self.callback = callback
        self.connection = connection
        
        if group == None:
            self.group_list.append(self)
            self.leader = self
        else:
            self.leader = group.check
            self.leader.group_list.append(self)

        self.connect("toggled", self.toggled_button)

    def toggled_button(self, widget):
        if widget.get_active():
            for i in self.leader.group_list:
                if not  i == widget and i.get_active() == True:
                    i.set_active(False)
            self.callback(self.connection)

class SettingButton(gtk.HBox):

    def __init__(self, group, connection,setting, callback):
        gtk.HBox.__init__(self)


        self.check = CheckButtonM(group, connection, callback)
        self.setting = setting

        self.pack_start(self.check, False, False)
        
        right_action_button_pixbuf = app_theme.get_pixbuf("Network/delete.png")
        self.right_button = ImageButton(right_action_button_pixbuf,
                                       right_action_button_pixbuf,
                                       right_action_button_pixbuf)
        #self.right_button.set_no_show_all(True)
        width = right_action_button_pixbuf.get_pixbuf().get_width()
        height = right_action_button_pixbuf.get_pixbuf().get_height()
        #hbox = gtk.EventBox()
        #hbox.set_visible_window(False)
        #hbox.connect("button-press-event", self.delete_setting, connection)
        #hbox.set_size_request(width, height)
        self.pack_end(self.right_button, False ,False, 0)
        self.right_button.connect("clicked", self.delete_setting, connection)
        #hbox.connect("enter-notify-event", self.enter_notify)
        #hbox.connect("leave-notify-event", self.leave_notify)
        self.show_all()
    
    def delete_setting(self, widget, connection):
        connection.delete()
        self.destroy()
        self.setting.destroy()

    def enter_notify(self, widget, event):
        pass
        #container_remove_all(widget)    
        #widget.add(self.right_button)
        #self.queue_draw()
        ##widget.show_all()
         
        #self.right_button.set_no_show_all(False)
        #self.right_button.show()
        #return False

    def leave_notify(self, widget, event):
        pass
        #container_remove_all(widget)    
        #self.right_button.hide()
        #return False

        
#class MyEntry(Entry):

    #def handle_button_press(self, widget, event):
        ## Select all when double click left button.
        #if is_double_click(event):
            #self.double_click_flag = True
            #self.grab_focus()
            #self.select_all()

#class SettingButton(gtk.EventBox):
    #HORIZONAL_PADDING = 10
    #VERITCAL_PADDING = 5

    #def __init__(self, group, connection, setting, callback): 
        ## Init
        #gtk.EventBox.__init__(self) 
        #self.setting = setting
        ##self.set_visible_window(False)
        #self.label = connection.get_setting("connection").id 
        #left_action_button_pixbuf = app_theme.get_pixbuf("Network/check_box.png") 
        #left_action_button_pixbuf_out = app_theme.get_pixbuf("Network/check_box_out.png") 
        #right_action_button_pixbuf = app_theme.get_pixbuf("Network/delete.png") 

        #self.left_width = left_action_button_pixbuf.get_pixbuf().get_width()
        #self.right_width = right_action_button_pixbuf.get_pixbuf().get_width()
        #self.height = left_action_button_pixbuf.get_pixbuf().get_height()

        ##self.left_button = ToggleButton(left_action_button_pixbuf_out, 
                                       ##left_action_button_pixbuf)
        #self.left_button = CheckButtonM(group, connection, callback)
        #self.right_button = ToggleButton(right_action_button_pixbuf,
                                       #right_action_button_pixbuf,
                                       #right_action_button_pixbuf)
        #self.entry = MyEntry()
        #self.entry.set_text(self.label)
        #self.entry.connect("press-return", self.return_pressed)
        #self.entry.show()

        #self.hbox = gtk.HBox()
        #left_align = gtk.Alignment(0, 0.5, 0, 0)
        #left_align.set_padding(0,0,self.HORIZONAL_PADDING, 0)
        #left_align.add(self.left_button)
        #self.hbox.pack_start(left_align, False , False ,0)

        #mid_align = gtk.Alignment(0.5,0.5,0,0)
        #mid_align.add(self.entry)
        #self.hbox.pack_start(mid_align, False, False, 0)

        #right_align = gtk.Alignment(0, 0.5, 0, 0)
        #right_align.set_padding(0,0,0,self.HORIZONAL_PADDING)
        #right_align.add(self.right_button)
        #self.hbox.pack_end(right_align, False, False, 0)
        #self.add(self.hbox)
        #self.show_all()
        ##self.hbox.connect("expose-event", self.expose_event)
        ##self.right_button.connect("clicked", self.delete_setting, connection)

        #self.set_events(gtk.gdk.BUTTON_PRESS_MASK|
                        #gtk.gdk.POINTER_MOTION_MASK)
        ##self.connect("button-press-event", self.button_press)

    #def return_pressed(self, widget):
        #widget.grab_focus_flag = False
        #widget.im.focus_out()
        #self.queue_draw()

    #def clicked_event(self, widget):
        #pass


    #def delete_setting(self, widget,connection):
        #print "safsdf"
        #connection.delete()
        #self.destroy()
        #self.setting.destroy()
        

    #def expose_event(self, widget, event):
        #cr = widget.window.cairo_create()
        #rect = widget.allocation
        #x, y, w, h = rect.x, rect.y, rect.width, rect.height

        ## Draw frame.
        #with cairo_disable_antialias(cr):
            #cr.set_line_width(1)
            #cr.set_source_rgb(*color_hex_to_cairo(ui_theme.get_color("combo_entry_frame").get_color()))
            #cr.rectangle(rect.x, rect.y, rect.width, rect.height)
            #cr.stroke()
            
            #cr.set_source_rgba(*alpha_color_hex_to_cairo((ui_theme.get_color("combo_entry_background").get_color(), 0.9)))
            #cr.rectangle(rect.x, rect.y, rect.width - 1, rect.height - 1)
            #cr.fill()

    #def set_size(self, width):
        #self.set_size_request(width, self.height + 2 * self.VERITCAL_PADDING)

        #self.entry.set_size_request(width - self.left_width - self.right_width- 2*self.HORIZONAL_PADDING , self.height + 2 * self.VERITCAL_PADDING)
        #padding = (self.left_width + self.right_width)/2 + self.HORIZONAL_PADDING
        ##self.entry.padding_x = padding 

        

if __name__ == "__main__":

    win = gtk.Window(gtk.WINDOW_TOPLEVEL)
    win.set_title("Main")
    win.set_size_request(770,500)
    win.set_border_width(11)
    win.set_resizable(True)
    win.connect("destroy", lambda w: gtk.main_quit())

    align = gtk.Alignment(1 , 1, 0,0)
    vbox = gtk.VBox()

    my_button = SettingButton("another setting")
    my_button.set_size(200)
    align.add(my_button)
    win.add(align)

    win.show_all()
    
    gtk.main()