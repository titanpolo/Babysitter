from discord.ext import commands

import discord

class Talks(commands.Cog):
    """Talks with User"""

    def __init__(self, client):
        self.client = client

    #quando o comando ".oi" for enviado responda Olá
    @commands.command(name="oi", help="Cumprimenta o bot. Argumentos: Nenhum")
    async def send_hello(self, ctx):
            name = ctx.author.name

            response = "Olá, " + name

            await ctx.send(response)

    #quando o comando ".dm" for enviado responda no privado
    @commands.command(name="dm", help="Manda mensagem padrão no PV. Argumentos: Nenhum")
    async def secret(self, ctx):
        try:
            await ctx.author.send("teste de dm")
        except discord.errors.Forbidden:
            await ctx.send("Não posso enviar mensagens, ligue a opção 'Permitir mensagens diretas de membros do servidor' (Opções > Privacidade e segurança)")

def setup(client):
    client.add_cog(Talks(client))

