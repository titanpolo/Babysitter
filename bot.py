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
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound

#bot token
TOKEN = os.environ["token"]

#bot construction (bot prefix)
client = commands.Bot(".")

#quando estiver pronto, faça:
@client.event
async def on_ready():
    print(f"{client.user} is online")
    #para saber onde está o canal o bot precisa estar logado antes de rodar "run"
    #current_time.start() #começar o relógio antes de rodar o bot

#quando uma mensagem for enviada faça:
@client.event
async def on_message(message):
    #para não entrar em loop das suas próprias mensagens
    if message.author == client.user:
        return
    #quando detectar a palavra "palavrão"
    if "palavrão" in message.content:
        await message.channel.send(
            f"Por favor, {message.author.name}, não ofenda os demais usuários!"
        )
        await message.delete()
    #evitar que o bot trave e os outros comandos parem de funcionar
    await client.process_commands(message)

#quando o comando "!oi" for enviado responda Olá
@client.command(name="oi", help="Cumprimenta o bot. Argumentos: Nenhum")
async def send_hello(ctx):
        name = ctx.author.name

        response = "Olá, " + name

        await ctx.send(response)

#quando o comando "!dm" for enviado responda no privado
@client.command(name="dm", help="Manda mensagem padrão no PV. Argumentos: Nenhum")
async def secret(ctx):
    try:
        await ctx.author.send("teste de dm")
    except discord.errors.Forbidden:
        await ctx.send("Não posso enviar mensagens, ligue a opção 'Permitir mensagens diretas de membros do servidor' (Opções > Privacidade e segurança)")

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

#gerador de embed com foto e formatação
@client.command(name="foto", help="Gera um embed padrão. Argumentos: Nenhum")
async def get_random_image(ctx):
    url_image = "https://picsum.photos/1920/1080"
    #construindo classe embed
    embed = discord.Embed(
        title = "Resultado da busca de imagem",
        description = "PS: A busca é totalmente aleatória",
        color = 0x0000FF
    )

    #definindo os atributos
    embed.set_author(name=client.user, icon_url=client.user.avatar_url) #autor
    embed.set_footer(text="Feito por " + client.user.name, icon_url=client.user.avatar_url) #rodapé

    embed.add_field(name ="API", value="Usamos a API do https://picsum.photos") #campo 1
    embed.add_field(name="Parâmetros", value="{largura}/{altura}") #campo 2
    embed.add_field(name="Exemplo", value=url_image, inline=False) #campo 3

    embed.set_image(url = url_image) #imagem

    await ctx.send(embed=embed)

#Consulta o preço de Cryptomoedas na Binance
@client.command(help="Consulta o preço de Cryptomoedas na Binance. Argumentos: moeda, par")
async def binance(ctx, coin, base):
    try:
        response = requests.get(
            f"https://api.binance.com/api/v3/ticker/price?symbol={coin.upper()}{base.upper()}"
        )

        data = response.json()
        price = data.get("price")

        if price:
            await ctx.send(f"Ovalor do par {coin}/{base} é {price}")
        else:
                await ctx.send(f"O par {coin}/{base} é inválido")
    except Exception as error:
        await ctx.send("Ops... Deu algum erro!")
        print(error)

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
@tasks.loop(seconds=2)
async def current_time():
    now = datetime.datetime.now()

    now = now.strftime("%d/%m/%Y às %H:%M:%S")

    channel = client.get_channel(926245089452384336)

    await channel.send("Data atual: " + now)
"""

#tratamento de erros, boas práticas, e ajuda (!help)
@client.event
async def on_command_error(ctx, error):
    if isinstance(error, MissingRequiredArgument): #se o erro for falta de argumentos
        await ctx.send("Favor enviar todos os Argumentos.")
    elif isinstance(error, CommandNotFound): #se o erro for comando inexistente
        await ctx.send("O comando não existe.")
    else:
        return
    ctx.send("Digite !help para ver os parâmetros de cada comando.")

client.run(TOKEN)

#para guardar variáveis do ambiente da pra usar o ".env" ou "decouple"