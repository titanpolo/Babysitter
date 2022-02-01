from discord.ext import commands

import discord

class Images(commands.Cog):
    """Works with Images"""

    def __init__(self, client):
        self.client = client


    #gerador de embed com foto e formatação
    @commands.command(name="foto", help="Gera um embed padrão. Argumentos: Nenhum")
    async def get_random_image(self, ctx):
        url_image = "https://picsum.photos/1920/1080"
        #construindo classe embed
        embed = discord.Embed(
            title = "Resultado da busca de imagem",
            description = "PS: A busca é totalmente aleatória",
            color = 0x0000FF
        )

        #definindo os atributos
        embed.set_author(name=self.client.user, icon_url=self.client.user.avatar_url) #autor
        embed.set_footer(text="Feito por " + self.client.user.name, icon_url=self.client.user.avatar_url) #rodapé

        embed.add_field(name ="API", value="Usamos a API do https://picsum.photos") #campo 1
        embed.add_field(name="Parâmetros", value="{largura}/{altura}") #campo 2
        embed.add_field(name="Exemplo", value=url_image, inline=False) #campo 3

        embed.set_image(url = url_image) #imagem

        await ctx.send(embed=embed)

def setup(client):
    client.add_cog(Images(client))

