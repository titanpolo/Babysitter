from discord.ext import commands

class Reactions(commands.Cog):
    """Works with Reactions"""

    def __init__(self, client):
        self.client = client

"""#em obras...
    @commands.Cog.listener()
    async def sample(self):
        print()

"""

def setup(client):
    client.add_cog(Reactions(client))

