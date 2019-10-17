#!/usr/bin/env python

import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk


class NewGameWindow(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("New game")
        self.connect("delete-event", Gtk.main_quit)
        self.set_border_width(10)

        self.name_entry = Gtk.Entry()
        self.name_entry.set_text("Default Save")
        self.name_entry.set_tooltip_text("Enter here the name under which you want to save this new game")

        self.name_entry_label = Gtk.Label()
        self.name_entry_label.set_label("Save name:")

        self.ok_button = Gtk.Button()
        self.ok_button.set_label("Create new save")
        self.ok_button.set_tooltip_text("Press to create your save with the above parameters")
        self.ok_button.connect("clicked", self.create_new_game, self.name_entry)

        self.layout = Gtk.Grid()
        self.layout.set_row_spacing(6)
        self.layout.set_column_spacing(6)

        self.layout.attach(self.name_entry_label, 0, 0, 1, 1)
        self.layout.attach(self.name_entry, 0, 1, 1, 1)
        self.layout.attach(self.ok_button, 0, 2, 1, 1)

        self.add(self.layout)

    def create_new_game(self, button, entry):
    exists = os.path.isfile("./saves/")


class StartScreen(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Dragon RPG") # TODO: Find better title
        self.connect("delete-event", Gtk.main_quit)
        self.set_border_width(10)

        self.layout = Gtk.Box()

        self.new_game_button = Gtk.Button(label="New Game")
        self.new_game_button.connect("clicked", self.create_new_game)

        self.layout.pack_start(self.new_game_button, True, True, 0)

        self.add(self.layout)

    def create_new_game(self, button):
        window = NewGameWindow()
        window.show_all()
        self.destroy()


if __name__ == "__main__":
    app = StartScreen()
    app.show_all()
    Gtk.main()
