# You can skip the generation of Model/Controller/Converter and Tests by supplying --bare to createcog

from .model import *
from settings import *


class NoscopeController:
    def __init__(self):
        pass

    def check_if_tracked_user(self, member):
        return True

    def check_ltp_channel(self, channel):
        if channel.id == DISCORD_LOOKING_TO_PLAY_CHANNEL_ID:
            return True

    def record_player(self, member):
        if Player.objects(dc_id=str(member.id)).count() > 0:
            return

        p = Player()
        p.display_name = member.display_name
        p.username = member.name
        p.dc_id = str(member.id)
        p.save()
