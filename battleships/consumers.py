from channels import Group
from channels.sessions import channel_session

import logging
logger = logging.getLogger(__name__)


@channel_session
def ws_add(message, game):
    #logger.info("player connected to web socket")
    Group('game-%s' % game).add(message.reply_channel)
    message.channel_session['game'] = game
    message.reply_channel.send({"accept": True})
    Group('game-%s' % game).send({
        'text': "Player connected to channel",
    })


@channel_session
def ws_echo(message):
    game = message.channel_session['game']
    Group('game-%s' % game).send({
        'text': message.content['text'],
    })
