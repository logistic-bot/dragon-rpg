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
            with open("./saves/{}.json".format(save_namee), "w"):
                pass # only create the file
                # TODO: Write initial data


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


if __name__ == "__main__":
    app = StartScreen()
    app.show_all()
    Gtk.main()
