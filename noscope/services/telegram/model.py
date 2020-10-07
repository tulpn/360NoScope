import random
import datetime

from mongoengine import *


class Poll(Document):

    poll_id = StringField()
    questions = ListField()
    message_id = IntField()
    chat_id = IntField()
    answers = IntField(default=0)
    closed = BooleanField(default=False)

    created_at = DateTimeField()
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

        return super(Poll, self).save(*args, **kwargs)


class PollAnswer(Document):

    poll_id = StringField()
    user_id = IntField()
    username = StringField()
    answer = ListField()

    created_at = DateTimeField()
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

        return super(PollAnswer, self).save(*args, **kwargs)
