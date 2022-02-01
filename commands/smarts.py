from discord.ext import commands

class Smarts(commands.Cog):
    """Works with Smart Commands"""

    def __init__(self, client):
        self.client = client

    #em obras...

def setup(client):
    client.add_cog(Smarts(client))

