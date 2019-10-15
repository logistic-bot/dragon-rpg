#!/usr/bin/env python

import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class AppWindow(Gtk.Window):
	def __init__(self):
		super().__init__()
		self.set_title("Dragon RPG") # TODO: Find better title
		self.connect("delete-event", Gtk.main_quit)


if __name__ == "__main__":
	app = AppWindow()
	app.show_all()
	Gtk.main()
