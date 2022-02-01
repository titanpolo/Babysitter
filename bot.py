#Vídeo aula q utilizei para aprender o básico
#É altamente recomendado assistir pelo menos o primeiro vídeo para configurar o bot e gerar um TOKEN
#https://www.youtube.com/watch?v=YWdchyTqt5I

#para rodar o bot localmente, deve ser preciso uma aplicação definida anteriormente e ser gerado um token, alem disso deve-se:
#instalar:  discord.py: para rodar a API
#           python-dotenv
#           requests: somente se quiser realizar acesso da API da binance definida na classe "cryptos.py"
#           nodemon: opicional, mas agiliza bastante no teste do código (compila auto sempre que salva o projeto)


import discord
from discord.ext import commands

import os

import dotenv
from dotenv import load_dotenv
load_dotenv()

#from collections import deque # ia usar isso pra fazer lista com manipulações O(1)

#bot token
TOKEN = os.environ["token"]

#bot construction (bot prefix)
intents = discord.Intents.all()

client = commands.Bot(".", intents=intents)


########### Automação do import de classes
def load_cogs(client):
    client.load_extension("manager")#carrega a classe manager
    client.load_extension("tasks.dates")#carrega a classe dates

    for file in os.listdir("commands"):#carrega todas as classes da pasta commands
        if file.endswith(".py"):
            cog = file[:-3]
            print(file)
            client.load_extension(f"commands.{cog}")


##executa o import de classes
load_cogs(client)


###converter texto dos arrays em linhas do field
def array_to_str(array):
    return "\n".join(str(x) for x in array)

##classe abstrata piloto q cria as arrays de controle
class Square:
    def __init__(self):

        self.field_names=["🟢Gold 1", "🔵Gold 2", "🟡Gold 3", "💚XP 1", "💙XP 2", "💛XP 3", "🟩Stone 1", "🟦Stone 2", "🟨Stone 3", "Waitlist"]


        self.gold1=[]
        self.gold2=[]
        self.gold3=[]
        self.xp1=[]
        self.xp2=[]
        self.xp3=[]
        self.stone1=[]
        self.stone2=[]
        self.stone3=[]
        self.wait=[]


## função que cria o embed de praca
def build_square_embed(square, title):

    str = "-"

    embed=discord.Embed(title = title, color = 0x0000FF)

    embed.add_field(name =square.field_names[0], value=str) #value n pode ser vazio ou ""
    embed.add_field(name =square.field_names[1], value=str)
    embed.add_field(name =square.field_names[2], value=str)

    embed.add_field(name =square.field_names[3], value=str)
    embed.add_field(name =square.field_names[4], value=str)
    embed.add_field(name =square.field_names[5], value=str)

    embed.add_field(name =square.field_names[6], value=str)
    embed.add_field(name =square.field_names[7], value=str)
    embed.add_field(name =square.field_names[8], value=str)

    embed.add_field(name =square.field_names[9], value=str)
    return embed

###Descobri um erro absurdo, tem q tratar o caso em que o usuário tentar usar o sistema de reação mas não tem nick de servidor
###o certo seria não permitir o usuário usar o sisteminha caso não tenha nick definido:
### por ex: quando ele reagir aparecerá "None" e vai bugar toda a lógica implementada,
### o certo seria ignorar o comando e não dar "append" nas variaveis globais

##variáveis globais de controle do bot
square_messages = []
square_queues = []

peak_messages = []
peak_queues = []

channels = []


@client.command(name="channel", help="Makes the channel visible/invisible to the bot. Arguments:\n<option>: on/off")
async def activate_channel(ctx, option):
    global channels
    if option in ["on", "off"]:
        print(option)
        channel = ctx.channel
        print(channel)
        if channel in channels:
            if option == "on":
                await ctx.send("Channel already online!")
            else:
                index = channels.index(channel)
                channels.pop(index)
                await ctx.send("Channel is now offline!")
        else:
            if option == "on":
                channels.append(channel)
                print("on now")
                await ctx.send("Channel is now online!")
            else:
                await ctx.send("Channel already offline!")
    else:
        await ctx.send("Wrong argument. Possible arguments: on/off")


#criar embed
@client.command(name="praca", help="Cria embed.")
async def create_embed(ctx, number):
    global square_messages, square_queues

    square = Square()

    print("square")

    msg = await ctx.send(embed=build_square_embed(square, f"Praça {number}"))

    print("msg")

    square_messages.append(msg)
    square_queues.append(square)

    print("appends")

    await msg.add_reaction("🟢")
    await msg.add_reaction("🔵")
    await msg.add_reaction("🟡")
    await msg.add_reaction("💚")
    await msg.add_reaction("💙")
    await msg.add_reaction("💛")
    await msg.add_reaction("🟩")
    await msg.add_reaction("🟦")
    await msg.add_reaction("🟨")

    print("bot reactions")

###funcao que remove elemento das arrays
def remove_from_list(nick, list):
    for x in range(len(list)):
        if list[x] == nick:
            list[x] = "-"
            break

##função para realizar busca em array
def find_or_not(item, list):
    if item in list: return list.index(item)
    return -1


#quando houver reação em alguma mensagem, faça:
@client.event
async def on_reaction_add(reaction, user, help="Adiciona usuario na fila"):
    global channels
    msg = reaction.message

    if not (msg.channel in channels): return #se o canal nao estiver online
    if user == client.user: return

    global square_messages, peak_messages

    i = find_or_not(msg, square_messages)

    embed = msg.embeds[0] #pega o primeiro embed da mensagem, cada mensagem tem uma array de embeds

    print(embed.title)

    if i > -1:
        global square_queues
        square = square_queues[i]
        print(square.field_names[0])
        print("embed")
        if reaction.emoji == "🟢":
            print("green")
            print(user.nick)
            square.gold1.append(user.nick)
            print(square.gold1[0])
            print(array_to_str(square.gold1))
            embed.set_field_at(0, name=square.field_names[0], value=array_to_str(square.gold1))
            print("field1")
        elif reaction.emoji == "🔵":
            square.gold2.append(user.nick)
            embed.set_field_at(1, name=square.field_names[1], value=array_to_str(square.gold2))
        elif reaction.emoji == "🟡":
            square.gold3.append(user.nick)
            embed.set_field_at(2, name=square.field_names[2], value=array_to_str(square.gold3))
        elif reaction.emoji == "💚":
            square.xp1.append(user.nick)
            embed.set_field_at(3, name=square.field_names[3], value=array_to_str(square.xp1))
        elif reaction.emoji == "💙":
            square.xp2.append(user.nick)
            embed.set_field_at(4, name=square.field_names[4], value=array_to_str(square.xp2))
        elif reaction.emoji == "💛":
            square.xp3.append(user.nick)
            embed.set_field_at(5, name=square.field_names[5], value=array_to_str(square.xp3))
        elif reaction.emoji == "🟩":
            square.stone1.append(user.nick)
            embed.set_field_at(6, name=square.field_names[6], value=array_to_str(square.stone1))
        elif reaction.emoji == "🟦":
            square.stone2.append(user.nick)
            embed.set_field_at(7, name=square.field_names[7], value=array_to_str(square.stone2))
        elif reaction.emoji == "🟨":
            square.stone3.append(user.nick)
            embed.set_field_at(8, name=square.field_names[8], value=array_to_str(square.stone3))
        #embed.set_field_at(9, name=square.field_names[9], value=array_to_str(square.wait))##o field waitlist pode ser removido futuramente
    else:
        i = find_or_not(msg, peak_messages)######################################### futuro pico
        if i < 0: return
        #peak = peak_messages[i]

    print("before await")
    await msg.edit(embed=embed)
    print("await")


#quando uma reação for removida, faça:
@client.event
async def on_reaction_remove(reaction, user):
    global channels
    msg = reaction.message

    if not (msg.channel in channels): return #se o canal nao for ativado
    if user == client.user: return

    global square_messages, peak_messages

    i = find_or_not(msg, square_messages)

    embed = msg.embeds[0]

    print(embed.title)
    ##esse tre
    if i > -1:
        global square_queues
        square = square_queues[i]
        if reaction.emoji == "🟢":
            j = find_or_not(user.nick, square.gold1)
            if j > -1:
                val = None
                square.gold1.remove(user.nick)
                if square.gold1 == []: val = "-"
                else: val = array_to_str(square.gold1)
                embed.set_field_at(0, name=square.field_names[0], value=val)
        elif reaction.emoji == "🔵":
            j = find_or_not(user.nick, square.gold2)
            if j > -1:
                val = None
                square.gold2.remove(user.nick)
                if square.gold2 == []: val = "-"
                else: val = array_to_str(square.gold2)
                embed.set_field_at(1, name=square.field_names[1], value=val)
        elif reaction.emoji == "🟡":
            j = find_or_not(user.nick, square.gold3)
            if j > -1:
                val = None
                square.gold3.remove(user.nick)
                if square.gold3 == []: val = "-"
                else: val = array_to_str(square.gold3)
                embed.set_field_at(2, name=square.field_names[2], value=val)
        elif reaction.emoji == "💚":
            j = find_or_not(user.nick, square.xp1)
            if j > -1:
                val = None
                square.xp1.remove(user.nick)
                if square.xp1 == []: val = "-"
                else: val = array_to_str(square.xp1)
                embed.set_field_at(3, name=square.field_names[3], value=val)
        elif reaction.emoji == "💙":
            j = find_or_not(user.nick, square.xp2)
            if j > -1:
                val = None
                square.xp2.remove(user.nick)
                if square.xp2 == []: val = "-"
                else: val = array_to_str(square.xp2)
                embed.set_field_at(4, name=square.field_names[4], value=val)
        elif reaction.emoji == "💛":
            j = find_or_not(user.nick, square.xp3)
            if j > -1:
                val = None
                square.xp3.remove(user.nick)
                if square.xp3 == []: val = "-"
                else: val = array_to_str(square.xp3)
                embed.set_field_at(5, name=square.field_names[5], value=val)
        elif reaction.emoji == "🟩":
            j = find_or_not(user.nick, square.stone1)
            if j > -1: 
                val = None
                square.stone1.remove(user.nick)
                if square.stone1 == []: val = "-"
                else: val = array_to_str(square.stone1)
                embed.set_field_at(6, name=square.field_names[6], value=val)
        elif reaction.emoji == "🟦":
            j = find_or_not(user.nick, square.stone2)
            if j > -1:
                val = None
                square.stone2.remove(user.nick)
                if square.stone2 == []: val = "-"
                else: val = array_to_str(square.stone2)
                embed.set_field_at(7, name=square.field_names[7], value=val)
        elif reaction.emoji == "🟨":
            j = find_or_not(user.nick, square.stone3)
            if j > -1:
                val = None
                square.stone3.remove(user.nick)
                if square.stone3 == []: val = "-"
                else: val = array_to_str(square.stone3)
                embed.set_field_at(8, name=square.field_names[8], value=val)
        
    await msg.edit(embed=embed)


client.run(TOKEN)

#para guardar variáveis do ambiente da pra usar o ".env" ou "decouple"
