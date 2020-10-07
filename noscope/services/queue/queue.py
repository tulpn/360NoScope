
from redis import Redis
from rq import Queue

from settings import *
from .tasks import send_voice_count

# Setup Queue
q = Queue(connection=Redis(host='redis', db=1))


def enqueue_action(action):
    """
    Enqueue action
    :param data: dict
    """
    data = {}
    if action['to'] == 'telegram':
        pass
    elif action['to'] == 'discord':
        pass

    if action['command'] == 'voice_count':
        pass

    try:
        q.enqueue(
            send_voice_count, data)
    except Exception as e:
        _logger.error(e)
