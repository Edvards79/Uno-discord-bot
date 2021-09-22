import discord

def info_embed(title, description):
    embedVar = discord.Embed(title=title, description=description, color=0x336eff)
    embedVar.set_thumbnail(url="https://image.flaticon.com/icons/png/512/189/189664.png")
    return embedVar

def warning_embed(title, description):
    embedVar = discord.Embed(title=title, description=description, color=0xff0000)
    embedVar.set_thumbnail(url="https://upload.wikimedia.org/wikipedia/commons/thumb/f/f7/Antu_dialog-warning.svg/1200px-Antu_dialog-warning.svg.png")
    return embedVar

def success_embed(title, description):
    embedVar = discord.Embed(title=title, description=description, color=0x00ff00)
    embedVar.set_thumbnail(url="https://cdn1.iconfinder.com/data/icons/color-bold-style/21/34-512.png")
    return embedVar