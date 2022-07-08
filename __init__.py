from mycroft import MycroftSkill, intent_handler
from mycroft.messagebus import Message
from .database.database import Database

class Fastnotes(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.db = Database()
        
    def initialize(self):
        self.log.info("0")
        self.add_event("fastnotes-skill:get_all_posts", self.handle_get_all_posts)
    
    def handle_get_all_posts(self, message):
        self.log.info(("HEJ!", message, type(message)))
        temp = self.db.get_all_posts()
        self.transmit_posts(temp)
        self.log.info(temp)
    
    def transmit_post(self, post:str):
        self.log.info(("HEJ", post, type(post)))
        self.bus.emit(Message("RELAY:MMM-FastNotes:NEW-POST", {"post": post}))
        
    def transmit_posts(self, posts:"list[str]"):
        self.bus.emit(Message("RELAY:MMM-FastNotes:ALL-POSTS", {"posts": posts}))
        
    def notify_delete_all_posts(self):
        self.bus.emit(Message("RELAY:MMM-FastNotes:DELETE-POSTS"))

    # When the utterance is complete.
    # E.g. 'Hey Mycroft, jot down that I should buy bananas'. (note: 'I should buy bananas')
    @intent_handler('take.note.intent')
    def take_note(self, message):
        note = message.data.get('note', None)
        if note is None:    # Make sure there's a note.
            return self.unspecified_note(message)
        self.db.create_post(note)
        self.speak_dialog("note.taken")
        return self.transmit_post(note)
        

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
            return self.transmit_post(note)
        else:
            self.speak_dialog('something.went.wrong')

    @intent_handler('clear.notepad.intent')
    def clear_notepad(self, message):
        if self.ask_yesno('are.you.sure') == 'yes':
            self.db.delete_all_posts()
            self.speak_dialog('notepad.cleared')
            return self.notify_delete_all_posts()
        else:
            self.speak_dialog('notepad.not.cleared')

def create_skill():
    return Fastnotes()