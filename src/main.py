#!/usr/bin/python3

import os
import argparse
import threading

import gi
gi.require_version("Gtk", "4.0")
from gi.repository import Gtk, GLib, GObject, Gio, Adw

#include errors.py
#include nbfc_client.py
#include subprocess_worker.py
#include common.py
#include gtk_common.py

class Globals(GObject.GObject):
    __gsignals__ = {
        "restart_service":      (GObject.SignalFlags.RUN_FIRST, None, (int,)),
        "model_config_changed": (GObject.SignalFlags.RUN_FIRST, None, ()),
    }

    is_root = (os.geteuid() == 0)
    nbfc_client = None

    def __init__(self):
        super().__init__()
        self.init() # TODO

    def init(self):
        self.nbfc_client = NbfcClient()

GLOBALS = Globals()
VERSION = "0.0.0"

#include widgets/about_widget.py
#include widgets/apply_buttons_widget.py
#include widgets/service_control_widget.py
#include widgets/basic_config_widget.py
#include widgets/fan_widget.py
#include widgets/fan_control_widget.py
#include widgets/sensor_widget.py
#include widgets/sensors_widget.py
#include widgets/update_widget.py
#include widgets/main_window.py

argp = argparse.ArgumentParser(
    prog='nbfc-gtk',
    description='Gtk-based GUI for NBFC-Linux')

argp.add_argument('--version', action='version', version=f'%(prog)s {VERSION}')

grp = argp.add_argument_group(title='Widgets')

grp.add_argument('--service',
    help='Start with service widget',
    dest='widget', action='store_const', const='service')

grp.add_argument('--fans',
    help='Start with fans widget',
    dest='widget', action='store_const', const='fans')

grp.add_argument('--basic',
    help='Start with basic configuration widget',
    dest='widget', action='store_const', const='basic')

grp.add_argument('--sensors',
    help='Start with sensors widget',
    dest='widget', action='store_const', const='sensors')

grp.add_argument('--update',
    help='Start with update widget',
    dest='widget', action='store_const', const='update')

opts = argp.parse_args()

class App(Gtk.Application):
    def __init__(self):
        super().__init__()

    def do_activate(self):
        win = MainWindow(self)

        if opts.widget is not None:
            win.setTabById(opts.widget)

        win.present()

app = App()
app.run()
