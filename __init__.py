from mycroft import MycroftSkill, intent_handler

class Fastnotes(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    # When the utterance is complete.
    # E.g. 'Hey Mycroft, jot down that I should buy bananas'. (note: 'I should buy bananas')
    @intent_handler('take.note.intent')
    def take_note(self, message):
        note = message.data.get('note', None)
        if note is None:    # Make sure there's a note.
            return self.unspecified_note(message)
        self.speak_dialog("note.taken")

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
        else:
            self.speak_dialog('something.went.wrong')

def create_skill():
    return Fastnotes()