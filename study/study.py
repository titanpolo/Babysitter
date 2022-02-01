#https://www.youtube.com/watch?v=YWdchyTqt5I
import requests

import discord
from discord.ext import commands, tasks

import os

import dotenv
from dotenv import load_dotenv
load_dotenv()

import datetime

#import das boas práticas e tratamento de erros



#bot token
TOKEN = os.environ["token"]

#bot construction (bot prefix)
intents = discord.Intents.all()

client = commands.Bot(".", intents=intents)


#dar cargos por reação
@client.event
async def on_reaction_add(reaction, user, help="Da cargos para as reações com 👍 e 💩. Argumentos: Nenhum"):
    #print(reaction.emoji)
    if reaction.emoji == "👍": #emoji da reação 1
        role = user.guild.get_role(934978316354609173) #id do cargo 1
        await user.add_roles(role) #colocar role
    if reaction.emoji == "💩": #emoji da reação 2
        role = user.guild.get_role(934978368749838376) #id do cargo 2
        await user.add_roles(role)


"""
@client.event
async def on_reaction_add(reaction, user):
    channel = reaction.message.channel
    await client.send_message(channel, '{} has added {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))

@client.event
async def on_reaction_remove(reaction, user):
    channel = reaction.message.channel
    await client.send_message(channel, '{} has removed {} to the message: {}'.format(user.name, reaction.emoji, reaction.message.content))

@client.command(pass_context=True)
async def clear(ctx, amount=100):
    channel = ctx.message.channel
    messages = []
    async for message in client.logs_from(channel, limit =int(amount)):
        messages.append(message)
    await client.delete_messages(messages)
*/
"""
"""

"""
client.run(TOKEN)

#para guardar variáveis do ambiente da pra usar o ".env" ou "decouple"