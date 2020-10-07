import random
import datetime

from mongoengine import *


class Game(Document):

    dc_id = StringField()
    title = StringField()

    created_at = DateTimeField()
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

        return super(Game, self).save(*args, **kwargs)


class GamingNight(Document):
    poll_id = StringField()  # reference to poll from telegram
    selected_date = DateTimeField()  # when it is happening

    created_at = DateTimeField()
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

        return super(GamingNight, self).save(*args, **kwargs)
