import discord
import re
import io

from Uno.Game import Game
from Uno.GUI import GUI
from Bot.commands import COMMANDS


class Bot(discord.Client):
    def __init__(self, channel_name):
        super().__init__()
        self.game = Game()
        self.commands = COMMANDS
        self.channel_name = channel_name

    async def on_ready(self):
        print('Logged on as ', self.user)

    async def on_message(self, message):
        if message.author == self.user:
            return
        if not hasattr(message.channel, "name") or message.channel.name == self.channel_name:
            await self.handle_message(message)
    
    async def handle_message(self, message):
        for regex in self.commands:
            if (re.match(regex, message.content, re.IGNORECASE)):
                if (not hasattr(message.channel, "name") and self.commands[regex]["in_dms"]
                    or hasattr(message.channel, "name") and self.commands[regex]["in_server"]
                    or self.commands[regex]["turn_required"] and self.game.is_turn(self.game.get_player_by_name(message.author.name))):

                    await self.commands[regex]["func"](message, self.game)

    @staticmethod
    async def show_players_view(game, player, text=None):
        table_img = GUI.generate_table_image(game)
        player_view_img = GUI.generate_player_view_image(player, table_img, text)
        with io.BytesIO() as image_binary:
            player_view_img.save(image_binary, 'PNG')
            image_binary.seek(0)
            await player.discord_handle.send(file=discord.File(fp=image_binary, filename='player_view.png'))

