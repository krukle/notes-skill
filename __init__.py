from mycroft import MycroftSkill, intent_handler


class Fastnotes(MycroftSkill):
    def __init__(self):
        MycroftSkill.__init__(self)

    @intent_handler('fastnotes.intent')
    def handle_fastnotes(self, message):
        self.speak_dialog('fastnotes')


def create_skill():
    return Fastnotes()

