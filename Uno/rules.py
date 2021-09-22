RULES = {
    "INITIAL_CARDS": {
        "desc": "How many cards to pick up at begining.",
        "value": 7
    },
    "MIN_PLAYERS": {
        "desc": "Min amount of players to start a game.",
        "value": 2
    },
    "MAX_PLAYERS": {
        "desc": "Max amount of players allowed in a game.",
        "value": 10
    },
    "DRAW_SKIP": {
        "desc": "Whether pickup cards (+2, +4) should also skip the next person\'s turn.",
        "value": True
    },
    "REVERSE_SKIP": {
        "desc": "Whether reverse cards skip turns when there\'s only two players left.",
        "value": True
    },
    "MUST_PLAY": {
        "desc": "Whether someone must play a card if they are able to.",
        "value": True
    },
    "AUTOPASS": {
        "desc": "Automatically proceeds to the next turn after drawing, meaning that you cannot play drawn cards.",
        "value": True
    },
    "NOT_SAY_UNO_CARDS": {
        "desc": "Amount of cards to pick up in case player doesn't say uno.",
        "value": 2
    }
}

def rules_to_string():
    rule_string = "----UNO RULES----\n"
    for i, RULE in enumerate(RULES):
        rule_string += f"{i}) {RULES[RULE]['desc'][:-1]}: {RULES[RULE]['value']}\n"
    return rule_string

