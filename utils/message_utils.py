from battleships.models.game import Message, InvalidMessage, FireMessage, MoveMessage, IdleMessage, Commands
from battleships.models.ship import Move
from channels import Group

TO = "TO"

# todo send user name as first arg!
# Accepts only messages in format:
# MOVE ship_name LEFT
# FIRE ship_name TO ship_name
# PASS
# MESSAGE message
#
# Any other message is considered as INVALID
def parse_message(raw_message)-> Message:
    list = raw_message.split()
    if 1 <= len(list):
        if list[0] == Commands.FIRE:
            if len(list) == 4 and list[2] == TO:
                message = FireMessage()
                message.attacker = list[1]
                message.defender = list[3]
                return message
            else:
                return InvalidMessage()
        elif list[0] == Commands.MOVE:
            if len(list) == 3:
                if list[2] == Move.FORWARD.value or list[2] == Move.BACKWARD.value or list[2] == Move.RIGHT.value or list[2] == Move.LEFT.value:
                    message = MoveMessage()
                    message.mover = list[1]
                    message.move_type = list[2]
                    return message
                else:
                    return InvalidMessage()
            else:
                return InvalidMessage()
        elif list[0] == Commands.PASS:
            if len(list) == 1:
                return IdleMessage()
            else:
                return InvalidMessage()
        elif list[0] == Commands.MESSAGE:
            message = Message()
            message.text = raw_message
            return message
        else:
            return InvalidMessage()
    else:
        return InvalidMessage()


def push_message(game_id, game_player_id, output_message):
    Group('game-%s' % game_id).send({
        'text': str(game_player_id) + ": " + output_message.toJSON(),
    })



