from mycroft import MycroftSkill, intent_handler
from mycroft.messagebus import Message
from .database.database import Database

class Notes(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)
        self.db = Database()
        
    def initialize(self):
        self.add_event("notes-skill:get_all_posts", self.handle_get_all_posts)
    
    def handle_get_all_posts(self, message):
        self.transmit_posts(self.db.get_all_posts())
    
    def transmit_post(self, post:"tuple[int, str, str]"):
        self.bus.emit(Message("RELAY:MMM-Notes:NEW-POST", {"post": post}))
        
    def transmit_posts(self, posts:"list[tuple[int, str, str]]"):
        self.bus.emit(Message("RELAY:MMM-Notes:ALL-POSTS", {"posts": posts}))
        
    def notify_delete_all_posts(self):
        self.bus.emit(Message("RELAY:MMM-Notes:DELETE-POSTS"))

    # When the utterance is complete.
    # E.g. 'Hey Mycroft, jot down that I should buy bananas'. (note: 'I should buy bananas')
    @intent_handler('take.note.intent')
    def take_note(self, message):
        note = message.data.get('note', None)
        if note is None:    # Make sure there's a note.
            return self.unspecified_note(message)
        self.speak_dialog("note.taken")
        return self.transmit_post(self.db.create_post(note))
        

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
            return self.transmit_post(self.db.create_post(note))
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
    return Notes()
