from battleships.models.game import Message, InvalidMessage, FireMessage, MoveMessage, IdleMessage, Commands
from battleships.models.ship import Move
from channels import Group

AT = "at"


# todo send user name as first arg!
# Accepts only messages in format:
# move ship_name [left,right,forth,back]
# fire ship_name at ship_name
# pass
# msg message
#
# Any other message is considered as INVALID
def parse_message(raw_message)-> Message:
    list = raw_message.split()
    if 1 <= len(list):
        if list[0] == Commands.FIRE:
            if len(list) == 4 and list[2] == AT:
                message = FireMessage(raw_message)
                message.attacker = list[1]
                message.defender = list[3]
                return message
            else:
                return InvalidMessage(raw_message)
        elif list[0] == Commands.MOVE:
            if len(list) == 3:
                if list[2] == Move.FORWARD.value or list[2] == Move.BACKWARD.value or list[2] == Move.RIGHT.value or list[2] == Move.LEFT.value:
                    message = MoveMessage(raw_message)
                    message.mover = list[1]
                    message.move_type = list[2]
                    return message
                else:
                    return InvalidMessage(raw_message)
            else:
                return InvalidMessage(raw_message)
        elif list[0] == Commands.PASS:
            if len(list) == 1:
                message = IdleMessage("Passes round")
                return message
            else:
                return InvalidMessage(raw_message)
        elif list[0] == Commands.MESSAGE:
            message = Message(raw_message)
            return message
        else:
            return InvalidMessage(raw_message)
    else:
        return InvalidMessage(raw_message)


def push_message(game_id, game_player_id, game_player_name, output_message):
    Group('game-%s' % game_id).send({
        'text': str(game_player_name) + ": " + output_message.toJSON(),
    })



