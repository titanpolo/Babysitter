from discord.ext import commands

import requests

class Cryptos(commands.Cog):
    """Works with Cryptos"""

    def __init__(self, client):
        self.client = client


    #Consulta o preço de Cryptomoedas na Binance
    @commands.command(help="Consulta o preço de Cryptomoedas na Binance. Argumentos: moeda, par")
    async def binance(self, ctx, coin, base):
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

def setup(client):
    client.add_cog(Cryptos(client))

