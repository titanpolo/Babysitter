from discord.ext import commands

class Tools(commands.Cog):
    """Usefull tools"""

    def __init__(self, client):
        self.client = client

    #em obras...

def setup(client):
    client.add_cog(Tools(client))

