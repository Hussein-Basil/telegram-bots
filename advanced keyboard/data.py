class Config:
    keyboards = {
        'Main Menu' : [['First', 'Second'], ['Third'],['Button Editor']],
        'First' : [['1'], ['2', '3'], ["Back","Main Menu"],['Button Editor']],
        'Second' : [['Files'], ['Albums', 'Voice Notes'], ["Back","Main Menu"],['Button Editor']],
        'Third' : [["Back","Main Menu"],['Button Editor']],
        'Files' : [["Back","Main Menu"],['Button Editor']],
        'Albums' : [["Back","Main Menu"],['Button Editor']],
        'Voice Notes' : [["Back","Main Menu"],['Button Editor']],
    }
    users = {}

class User:
    def __init__(self, chat_id):
        self.id = chat_id
        self.steps = ["Main Menu"]
        Config.users[self.id] = self.steps
