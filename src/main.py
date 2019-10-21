#!/usr/bin/env python

# increment this counter each time you refactor this file
# n=0

"""
This is the main (and currently the only) file of this project.
E V E R Y T H I N G  is happening in this file, from initialisation to running,
to error handeling.
TODO: Add explanation about how each class in this file is interacting with the
others.
"""

import os
import gi
gi.require_version("Gtk", "3.0")
from gi.repository import Gtk # TODO: find a way so pylint inglores C0413 on this line


class StartScreen(Gtk.Window):
    """
    This window is shown when the app starts up.
    It will contains buttons to load a game, create a new game, and possibly others.

    At the momment, it only contains a "New Game" button, and when clicked
    spawns a "NewGameWindow" Windows
    """
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
        """
        This method opens a NewGameWindow and destroys itself.
        it is used to create new game
        """
        button.set_label("Please wait...")
        window = NewGameWindow()
        window.show_all()
        self.destroy()


class NewGameWindow(Gtk.Window):
    """
    This window is spawned by StartScreen and allows the user to create a new game.
    It uses ConfirmOverwriteDialog if the user is about to overwrite a save, and
    spawns GameWindow to allow the user to start playing
    """
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
        """
        This method creates the game file, using ConfirmOverwriteDialog if the
        user attemts to overwrite a saved game
        """
        button.set_label("Please wait...")
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
        """
        This method uses ConfirmOverwriteDialog to ask the user if he is certain
        that he wants to overide a save
        """
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
    """
    This window displays a warning to the user when he is about to overwrite a save.
    """
    def __init__(self, parent, save_name):
        Gtk.Dialog.__init__(self, "Confirm Overwrite", parent, 0, (
            Gtk.STOCK_CANCEL, Gtk.ResponseType.CANCEL, Gtk.STOCK_OK, Gtk.ResponseType.OK))
        self.set_default_size(150, 100)

        text = """You are about to overwrite the save `{}`.
Are you sure you want to do that?""".format(save_name)
        label = Gtk.Label(label=text)

        box = self.get_content_area()
        box.add(label)
        self.show_all()


class GameWindow(Gtk.Window):
    """
    This is the window where the game is played.
    It has a function for each chapter
    """
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
        # TODO: Find a way to make the text wrap when there is not enough space in the window

        self.layout = Gtk.Grid()
        self.layout.set_row_homogeneous(True)
        self.layout.set_column_homogeneous(True)
        self.layout.attach(self.story_box, 0, 0, 1, 1)

        self.add(self.layout)

        self.chapter_1()

    def on_game_closed(self, *args):
        """
        This method is called when the game is closed.
        It is still a work-in-progress
        """
        # # WARNING: WORK-IN-progress
        # *args is ignored but necessary because for some reason, in __init__
        # the self.connect gives 3 args to on_game_closed, don't know why...
        Gtk.main_quit() # TODO: add a warning for the user that any unsaved progress will be lost
        # TODO: add a save_game function
        # TODO: make the game auto_save a the start of each chapter

    def advance_story(self, message, saying_to_self=False, clear=False, tutorial=False, no_dot=False):
        """
        This function is used to display story elements to the player.
        you can use no_dot=True to stop the function to add a leading dot

        Usage:
        advance_story("Some text message") # Will display ` > Some text message.`
        # notice how by default, it will display the message as a game message.

        advance_story("Some text message", saying_to_self=True)
        # will display `«Some text message...»`
        # this is used for internal toughts of the protagonist

        advance_story("Some text message", clear=True) # will display `Some text message`
        # this is used for unusual messages, without any decoration

        advance_story("Some text message", tutorial=True)
        # will display `[Tutorial] Some text message.`
        # this is used for help messages for the player

        TODO: add a way to make the message be said by someone else than the tutorial
        """
        end_iter = self.story_box_buffer.get_end_iter()
        if no_dot:
            end_to_all_messages = "\n"
        else:
            end_to_all_messages = ".\n"

        if saying_to_self:
            self.story_box_buffer.insert(end_iter, "\t\t\t«" + message + "...»\n")
        elif clear:
            self.story_box_buffer.insert(end_iter, "\t\t" + message + "\n")
        elif tutorial:
            self.story_box_buffer.insert(end_iter, "[Tutorial]\t" + message + end_to_all_messages)
        else:
            self.story_box_buffer.insert(end_iter, " > " + message + end_to_all_messages)

    def chapter_1(self):
        """
        This function is executed so that the player can play the first chapter.
        It contains everything, from story to choises.
        """
        self.advance_story("Chapter 1: The beginning")
        self.advance_story("Well, here I am", True)
#        sleep(1)
        self.advance_story("\t...", clear=True)
#        sleep(1)
        self.advance_story("As you may have guessed, you are a Dragon", tutorial=True)
        self.advance_story("In this world, Dragons are very respected, and are \
living in the same towns as humans, although not always very \
peacefully..", tutorial=True)
        self.advance_story("But let's start the game, shall we?", tutorial=True, no_dot=True)

if __name__ == "__main__":
    APP = StartScreen()
    APP.show_all()
    Gtk.main()
