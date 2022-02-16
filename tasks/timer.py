from discord.ext import commands, tasks

import datetime


class Timer(commands.Cog):
    """Works with time"""

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.current_time.start()


        
    @tasks.loop(hours=1)
    async def current_time(self):
        now = datetime.datetime.now()

        now = now.strftime("%d/%m/%Y às %H:%M:%S")

        channel = self.client.get_channel(937818770116862032)

        await channel.send("Data atual: " + now)

def setup(client):
    client.add_cog(Timer(client))


"""
class Dates(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.Cog.listener()
    async def on_ready(self):
        self.current_time.start()


        
    @tasks.loop(hours=1)
    async def current_time(self):
        now = datetime.datetime.now()

        now = now.strftime("%d/%m/%Y às %H:%M:%S")

        channel = self.client.get_channel(937818770116862032)

        await channel.send("Data atual: " + now)

def setup(client):
    client.add_cog(Dates(client))
"""