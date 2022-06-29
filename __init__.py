from tkinter import N
from mycroft import MycroftSkill, intent_handler
from pathlib import Path 
import os
import sys
DB_DIR = os.path.join(
    str(Path.home()), 'MagicMirror', 'modules', 'MMM-FastNotes', 'backend')
sys.path.append(DB_DIR)
from database import Database

YES = ('yes', 'ja')
NO  = ('no', 'nej')

class Fastnotes(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.db = Database()

    # When the utterance is complete.
    # E.g. 'Hey Mycroft, jot down that I should buy bananas'. (note: 'I should buy bananas')
    @intent_handler('take.note.intent')
    def take_note(self, message):
        note = message.data.get('note', None)
        if note is None:    # Make sure there's a note.
            return self.unspecified_note(message)
        self.speak_dialog("note.taken")
        self.db.create_post(note)

    # When the utterance is missing a note.
    # E.g: 'Hey Mycroft, take a note'. 
    @intent_handler('what.should.i.jot.intent')
    def unspecified_note(self, message):
        note = message.data.get('note', None)
        if note is not None:    # Make sure there's no note.
            return self.take_note(message)
        note = self.get_response('what.should.i.jot')
        if note is not None: 
            self.speak_dialog('note.taken')
            self.db.create_post(note)
        else:
            self.speak_dialog('something.went.wrong')

    @intent_handler('clear.notepad.intent')
    def clear_notepad(self, message):
        is_sure = self.ask_yesno('are.you.sure')
        if is_sure in YES:
            self.speak_dialog('notepad.cleared')
            self.db.delete_all_posts()
        elif is_sure in NO:
            self.speak_dialog('notepad.not.cleared')
        else:
            self.speak_dialog('could.not.understand')

def create_skill():
    return Fastnotes()