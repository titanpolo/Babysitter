from discord.ext import commands

class Channels(commands.Cog):
    """Works with the Channels"""

    def __init__(self, client):
        self.client = client

    ###em obras...    

def setup(client):
    client.add_cog(Channels(client))

