from tkinter import N
from mycroft import MycroftSkill, intent_handler
from mycroft.messagebus import Message
from pathlib import Path 
import os
import sys
DB_DIR = os.path.join(
    str(Path.home()), 'MagicMirror', 'modules', 'MMM-FastNotes', 'backend')
sys.path.append(DB_DIR)
from database import Database

class Fastnotes(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.db = Database()
        
    def notify_mirror(self):
        self.bus.emit(Message("RELAY:MMM-FastNotes:DB-UPDATED"))

    # When the utterance is complete.
    # E.g. 'Hey Mycroft, jot down that I should buy bananas'. (note: 'I should buy bananas')
    @intent_handler('take.note.intent')
    def take_note(self, message):
        note = message.data.get('note', None)
        if note is None:    # Make sure there's a note.
            return self.unspecified_note(message)
        self.db.create_post(note)
        self.speak_dialog("note.taken")
        return self.notify_mirror()
        

    # When the utterance is missing a note.
    # E.g: 'Hey Mycroft, take a note'. 
    @intent_handler('what.should.i.jot.intent')
    def unspecified_note(self, message):
        note = message.data.get('note', None)
        if note is not None:    # Make sure there's no note.
            return self.take_note(message)
        note = self.get_response('what.should.i.jot')
        if note is not None: 
            self.db.create_post(note)
            self.speak_dialog('note.taken')
            return self.notify_mirror()
        else:
            self.speak_dialog('something.went.wrong')

    @intent_handler('clear.notepad.intent')
    def clear_notepad(self, message):
        if self.ask_yesno('are.you.sure') == 'yes':
            self.db.delete_all_posts()
            self.speak_dialog('notepad.cleared')
            return self.notify_mirror()
        else:
            self.speak_dialog('notepad.not.cleared')

def create_skill():
    return Fastnotes()