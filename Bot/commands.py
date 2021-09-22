import Bot.embeds as embeds
from Bot import Bot
from Uno.Deck import Card
from Uno.rules import RULES


async def _help(message, game):
    help_string = ""
    for regex in COMMANDS:
        if COMMANDS[regex]["visible"]:
            regex_desc = COMMANDS[regex]["desc"]
            help_string += f"**{regex}**: {regex_desc}\n"
        
    help_string += "\nTo put a card say it's value and color delimited by coma, eg. 4,yellow. Tu put wild cards and choose a color say wild,green or +4,yellow."
    await message.channel.send(embed=embeds.info_embed("Available commands", help_string))

async def _rules(message, game):
    rule_string = ""
    for i, rule_name in enumerate(RULES):
        rule_value = RULES[rule_name]["value"]
        rule_desc = RULES[rule_name]["desc"]
        rule_string += f"{i}) {rule_name.lower()}: **{rule_value}** ({rule_desc}) \n"

    await message.channel.send(embed=embeds.info_embed("Rules", rule_string))
    
async def _add_player(message, game):
    ret = game.add_player(message.author.name, message.author)

    player_list = "Players joined: \n"+"\n".join([f"`{player.name}`" for player in game.playerCycle.items])

    if "success" in ret.keys():
        await message.channel.send(embed=embeds.success_embed(ret["success"], player_list))
    elif "error" in ret.keys():
        await message.channel.send(embed=embeds.warning_embed(ret["error"], ""))

async def _start_game(message, game):
    ret = game.start()
    if "success" in ret.keys():
        await message.channel.send(embed=embeds.success_embed(ret["success"], ""))
        for p in game.playerCycle.items: await Bot.Bot.show_players_view(game, p, f"Game has started! It's {game.current_player.name}'s turn.")        
    elif "error" in ret.keys():
        await message.channel.send(embed=embeds.warning_embed(ret["error"], ""))

async def _draw_card(message, game):
    player = game.get_player_by_name(message.author.name)
    ret = game.draw_card(player)
    if "success" in ret.keys():
        for p in game.playerCycle.items: await Bot.Bot.show_players_view(game, p, ret["success"])
    elif "error" in ret.keys():
        await Bot.Bot.show_players_view(game, player, ret["error"])

async def _play_card(message, game):
    value, colour = message.content.lower().strip().split(",")
    value = value.strip()
    colour = colour.strip()
    if colour not in Card.COLOURS:
        await message.channel.send(embed=embeds.info_embed("Help", "Remember to put a card say it's value and color delimited by coma, eg. 4,yellow. Tu put wild cards and choose a color say wild,green or +4,yellow."))
        return

    player = game.get_player_by_name(message.author.name)

    if value == Card.CARD_DRAW_FOUR or value == Card.CARD_WILD:
        card = Card(value, None)
        ret = game.play_card(player, card, colour)
    else:
        card = Card(value, colour)
        ret = game.play_card(player, card)
    
    if "success" in ret.keys():
        for p in game.playerCycle.items: await Bot.Bot.show_players_view(game, p, ret["success"])
    elif "error" in ret.keys():
        await Bot.Bot.show_players_view(game, player, ret["error"])

async def _say_uno(message, game):
    player = game.get_player_by_name(message.author.name)
    if len(player.hand) == 1:
        player.has_said_uno = True

async def _say(message, game):
    player = game.get_player_by_name(message.author.name)
    message = message.content.replace("say ", "")
    players_to_send = [p for p in game.playerCycle.items if p != player]
    for p in players_to_send: await p.discord_handle.send(embed=embeds.info_embed(f"Message from {player.name}", message))
    await player.discord_handle.send(embed=embeds.success_embed(f"Success!", "Message has been sent"))
    


COMMANDS = {
    "help": {"desc": "Get list of available commands", "func": _help, "turn_required": False, "in_dms": True, "in_server": True, "visible": True},
    "rules": {"desc": "Print out the rules of the game", "func": _rules, "turn_required": False, "in_dms": True, "in_server": True, "visible": True},
    "join": {"desc": "Join the game", "func": _add_player, "turn_required": False, "in_dms": False, "in_server": True, "visible": True},
    "start": {"desc": "Start the game", "func": _start_game, "turn_required": False, "in_dms": False, "in_server": True, "visible": True},
    "draw": {"desc": "Draw a card from the deck", "func": _draw_card, "turn_required": True, "in_dms": True, "in_server": False, "visible": True},
    ".*,.*": {"desc": "Play a card", "func": _play_card, "turn_required": True, "in_dms": True, "in_server": False, "visible": False},
    "uno": {"desc": "Say uno", "func": _say_uno, "turn_required": True, "in_dms": True, "in_server": False, "visible": True},
    "say .*": {"desc": "Broadcast a message to all the players", "func": _say, "turn_required": False, "in_dms": True, "in_server": False, "visible": True},
}
