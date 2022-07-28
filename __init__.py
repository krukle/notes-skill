from mycroft import MycroftSkill, intent_handler
from mycroft.messagebus import Message
from .database.database import Database

class Notes(MycroftSkill):
    def __init__(self):
        """
        Initialize the skill. Load the database.
        """
        MycroftSkill.__init__(self)
        self.db = Database()
        
    def initialize(self):
        """
        This is called when the skill is first loaded. Subscribe to MMM-Notes notification to fetch all posts from database.
        """
        self.add_event("notes-skill:get_all_posts", self.handle_get_all_posts)
    
    def handle_get_all_posts(self, message):
        """
        Handle the get all posts message. Retrieve all posts from the database and transmit them.
        """
        self.transmit_posts(self.db.get_all_posts())
    
    def transmit_post(self, post:"tuple[int, str, str]"):
        """
        Transmit a post to the MMM-Notes module.
        @param post - the post to transmit
        """
        self.bus.emit(Message("RELAY:MMM-Notes:NEW-POST", {"post": post}))
        
    def transmit_posts(self, posts:"list[tuple[int, str, str]]"):
        """
        Transmit the posts to the MMM-Notes module.
        @param posts - the posts to transmit
        """
        self.bus.emit(Message("RELAY:MMM-Notes:ALL-POSTS", {"posts": posts}))
        
    def notify_delete_all_posts(self):
        """
        Notify the MMM-Notes module to delete all posts.
        """
        self.bus.emit(Message("RELAY:MMM-Notes:DELETE-POSTS"))

    # When the utterance is complete.
    # E.g. 'Hey Mycroft, jot down that I should buy bananas'. (note: 'I should buy bananas')
    @intent_handler('take.note.that.intent')
    def take_note(self, message):
        """
        This function is called when the user asks for a note and specifies the note. It will take the note and store it in the database.
        @param message - the message containing the note
        """
        note = message.data.get('note', None)
        if note is None:  
            return self.unspecified_note(message)
        self.speak_dialog("note.taken")
        return self.transmit_post(self.db.create_post(note))
        

    # When the utterance is missing a note.
    # E.g: 'Hey Mycroft, take a note'. 
    @intent_handler('take.note.intent')
    def unspecified_note(self, message):
        """
        This function is called when the user asks for a note without specifying the note. It will take the note and store it in the database.
        @param message - the message not containing the note
        @returns the response from the database
        """
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
        """
        This function is called when the user asks to clear the notepad. Asks for user confirmation and clears the notepad.
        """
        if self.ask_yesno('are.you.sure') == 'yes':
            self.db.delete_all_posts()
            self.speak_dialog('notepad.cleared')
            return self.notify_delete_all_posts()
        else:
            self.speak_dialog('notepad.not.cleared')

def create_skill():
    return Notes()
