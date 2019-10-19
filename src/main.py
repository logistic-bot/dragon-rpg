#!/usr/bin/env python

# increment this counter each time you refactor this file
# n=0

import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk

class StartScreen(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Dragon RPG")  # TODO: Find better title
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

class NewGameWindow(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("New game")
        self.connect("delete-event", Gtk.main_quit)
        self.set_border_width(10)

        self.name_entry = Gtk.Entry()
        self.name_entry.set_text("Default Save")
        self.name_entry.set_tooltip_text(
            "Enter here the name under which you want to save this new game")

        self.name_entry_label = Gtk.Label()
        self.name_entry_label.set_label("Save name:")

        self.ok_button = Gtk.Button()
        self.ok_button.set_label("Create new save")
        self.ok_button.set_tooltip_text(
            "Press to create your save with the above parameters")
        self.ok_button.connect(
            "clicked", self.create_new_game, self.name_entry)

        self.layout = Gtk.Grid()
        self.layout.set_row_spacing(6)
        self.layout.set_column_spacing(6)

        self.layout.attach(self.name_entry_label, 0, 0, 1, 1)
        self.layout.attach(self.name_entry, 0, 1, 1, 1)
        self.layout.attach(self.ok_button, 0, 2, 1, 1)

        self.add(self.layout)

    def create_new_game(self, button, entry):
        save_name = entry.get_text()
        exists = os.path.isfile("./saves/{}.json".format(save_name))

        do_owerwrite = True # By default, there is nothing to owerwrite

        if exists:
            do_owerwrite = self.confirm_overide_save(save_name)

        if do_owerwrite:
            with open(os.path.abspath("./saves/{}.json".format(save_name)), "w+"):
                pass # only create the file

        window = GameWindow()
        window.show_all()
        self.destroy()

    def confirm_overide_save(self, save_name):
        confirm_dialog = ConfirmOverwriteDialog(self, save_name)
        response = confirm_dialog.run()
        confirm_dialog.destroy()

        if response == Gtk.ResponseType.OK:
            return True # Overwrite
        elif response == Gtk.ResponseType.CANCEL:
            return False # Do not overwrite
        else:
            raise Exception("Can't handle unkown dialog reponse " + response)

class ConfirmOverwriteDialog(Gtk.Dialog):
    def __init__(self, parent, save_name):
        Gtk.Dialog.__init__(self, "Confirm Overwrite", parent, 0, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)

        label = Gtk.Label(
            label="You are about to overwrite the save `{}`.\nAre you sure you want to do that?".format(save_name))

        box = self.get_content_area()
        box.add(label)
        self.show_all()

class GameWindow(Gtk.Window):
    def __init__(self):
        super().__init__()
        self.set_title("Dragon RPG")
        self.connect("delete-event", self.on_game_closed)
        self.set_border_width(10)

        self.story_box = Gtk.TextView()
        self.story_box.set_editable(False)
        self.story_box.set_cursor_visible(False)
        self.story_box_buffer = self.story_box.get_buffer()
        self.advance_story("Welcome to the Dragon RPG")

        self.layout = Gtk.Grid()
        self.layout.set_row_homogeneous(True)
        self.layout.set_column_homogeneous(True)
        self.layout.attach(self.story_box, 0, 0, 1, 1)

        self.add(self.layout)

        self.chapter_1()

    def on_game_closed(self, *args): # *args is ignored but necessary because for some reason, in __init__ the self.connect gives 3 args to on_game_closed, don't know why...
        Gtk.main_quit()

    def advance_story(self, message, saying_to_self=False, clear=False, tutorial=False):
        end_iter = self.story_box_buffer.get_end_iter()

        if saying_to_self:
            self.story_box_buffer.insert(end_iter, "\t\t\t«" + message + "...»\n")
        elif clear:
            self.story_box_buffer.insert(end_iter, "\t\t" + message + "\n")
        elif tutorial:
            self.story_box_buffer.insert(end_iter, "[Tutorial]\t" + message + ".\n")
        else:
            self.story_box_buffer.insert(end_iter, " > " + message + ".\n")

    def chapter_1(self):
        self.advance_story("Chapter 1: The beginning")

if __name__ == "__main__":
    app = StartScreen()
    app.show_all()
    Gtk.main()
