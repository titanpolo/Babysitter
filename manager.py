from discord.ext import commands
from discord.ext.commands.errors import MissingRequiredArgument, CommandNotFound


class Manager(commands.Cog):
    """Manage the client"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        print(f"{self.client.user} is online")   

    #quando uma mensagem for enviada faça:
    @commands.Cog.listener()
    async def on_message(self, message):
        #para não entrar em loop das suas próprias mensagens
        if message.author == self.client.user:
            return
        #quando detectar a palavra "palavrão"
        if "palavrão" in message.content:
            await message.channel.send(
                f"Por favor, {message.author.name}, não ofenda os demais usuários!"
            )
            await message.delete()
        #evitar que o bot trave e os outros comandos parem de funcionar

    #tratamento de erros, boas práticas, e ajuda (.help)
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, MissingRequiredArgument): #se o erro for falta de argumentos
            await ctx.send("Favor enviar todos os Argumentos.")
        elif isinstance(error, CommandNotFound): #se o erro for comando inexistente
            await ctx.send("O comando não existe.")
        else:
            return
        await ctx.send("Digite '.help <comando>' para ver os parâmetros de cada comando.")


def setup(client):
    client.add_cog(Manager(client))

