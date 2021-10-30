""" dating app
create a method to return a new, random candidate
- must not show the same person
- must not show the someone that user has already swiped on
- when a user swipes right...
  - if the other user like them: send both a message with contact info
  - if the other user dislike them: let user down gently
  - if the other user hasn't evaluated yet: display "give it time" message
 """
import json

def get_json(filename):
    try:
        return json.loads(open(filename).read())
    except (IOError, ValueError):
        return ""


def send_email(person):
    pass

def let_down_gently(person):
    pass

def give_it_time(person):
    pass

class Application():
    def get_random_person(self):
        pass

    # FUT1
    def get_next_person(self, user):
        person = self.get_random_person()
        while person in user['people_seen']:
            person = self.get_random_person()
        return person

    # FUT2
    def evaluate(self, person1, person2):
        if person1 in person2['likes']:
            send_email(person1)
            send_email(person2)
        elif person1 in person2['dislikes']:
            let_down_gently(person1)
        elif person1 not in person2['likes'] and person1 not in person2['dislikes']:
            give_it_time(person1)
