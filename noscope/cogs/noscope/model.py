import random
import datetime

from mongoengine import *


class Player(Document):

    display_name = StringField()
    username = StringField()
    dc_id = StringField()

    created_at = DateTimeField()
    updated_at = DateTimeField(default=datetime.datetime.now)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = datetime.datetime.now()
        self.updated_at = datetime.datetime.now()

        return super(Player, self).save(*args, **kwargs)
