import discord
from discord.ext import commands

import asyncio



class Discord(commands.Cog):
    def __init__(self,bot):
        self.bot = bot


    # api finder command
    @commands.command()
    async def find(self,ctx,*,api=None):

        if api is None:
            await ctx.send('Include what you want me to find.')

        html = ("https://discordpy.readthedocs.io/en/latest/api.html#" + api)
        await ctx.reply(f"Here's your requested material:\n{html}", mention_author=False)
    
    # reference command
    @commands.command(aliases=['refer'])
    async def reference(self,ctx):
        await ctx.send('API reference: https://discordpy.readthedocs.io/en/latest/api.html')

    @commands.command()
    async def tags(self, ctx):
        await ctx.send(embed=discord.Embed(description='**List of tags:**\n`status`\n`activity`\n`code`\n`type`\n`music`\n\nUse `?tag <tag>` to view the tag', color=discord.Color.random()))

    @commands.group(invoke_without_command=True, hidden=True)
    async def tag(self, ctx):
        await ctx.send('Please provided a tag!\nUse `?tags` for a list of tags')
            

    @tag.command()
    async def status(self, ctx):
        msg = '<:s_Online:827276470148923392> <:s_Idle:827276518551977984> <:s_Dnd:827276569680543844> <:s_Invis:827276650336747520>\n```py\n# Online\nawait bot.change_presence(status=discord.Status.online)\n\n# Idle\nawait bot.change_presence(status=discord.Status.idle)\n\n# Do Not Disturb\nawait bot.change_presence(status=discord.Status.dnd)\n\n# Invisible\nawait bot.change_presence(status=discord.Status.offline)\n```'
        if ctx.message.reference:
            reply = ctx.message.reference.resolved
            await reply.reply(msg)
        else:
            await ctx.reply(msg, mention_author=False)

    @tag.command(aliases=['presence', 'rp', 'rich_presence'])
    async def activity(self, ctx):
        await ctx.reply('```py\n# Playing\nawait bot.change_presence(activity=discord.Game(name="a game"))\n\n# Streaming\nawait bot.change_presence(activity=discord.Streaming(name="My Stream", url="https://twitch.tv/settings"))\n\n# Listening\nawait bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))\n\n# Watching\nawait bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))\n\n# Competing\nawait bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name="eSports"))\n```', mention_author=False)

    # code blocks command
    @tag.command(aliases=['codeblocks','blocks'])
    async def code(self,ctx):
        if ctx.message.reference:
            if ctx.message.reference.cached_message is None:
                channel = self.bot.get_channel(ctx.message.reference.channel_id)
                msg = await channel.fetch_message(ctx.message.reference.message_id)

            else:
                msg = ctx.message.reference.cached_message
        em = discord.Embed(
            title = 'Using code blocks in python. \nHere\'s how to format Python code on Discord:',
            description = "**Input:**\n\```py\nprint('Hello world!')\n\```\n**Output:**\n```py\nprint('Hello world')```\n\nThese are backticks, not quotes. Check [this](https://superuser.com/questions/254076/how-do-i-type-the-tick-and-backtick-characters-on-windows/254077#254077) out if you can't find the backtick key.",
            color = discord.Color.random()
        )
        await msg.reply(embed=em, mention_author=False)
    
    # How to type
    @tag.command()
    async def type(self,ctx):
        if ctx.message.reference:
            if ctx.message.reference.cached_message is None:
                channel = self.bot.get_channel(ctx.message.reference.channel_id)
                msg = await channel.fetch_message(ctx.message.reference.message_id)

            else:
                msg = ctx.message.reference.cached_message
        async with ctx.typing():
            await asyncio.sleep(1.5)
        await msg.reply("<a:type:826891270634340384> **Discord.py helper** is typing...\n```py\nimport asyncio\n\n@bot.command()\nasync def command_name(ctx):\n    async with ctx.typing():\n        # Do stuff here\n        await asyncio.sleep(x)\n    await ctx.send('Message here.')\n```", mention_author=False)

    @tag.command()
    async def music(self,ctx):
        if ctx.message.reference:
            if ctx.message.reference.cached_message is None:
                channel = self.bot.get_channel(ctx.message.reference.channel_id)
                msg = await channel.fetch_message(ctx.message.reference.message_id)

            else:
                msg = ctx.message.reference.cached_message
        await msg.reply('Want to make an easy Music bot?\nThen DiscordUtils is the perfect thing for you.\nDocs: <https://docs.discordutils.gq/music>\nGithub: <https://github.com/toxicrecker/DiscordUtils>', mention_author=False)

    # links command 
    @commands.command()
    async def links(self,ctx):
        em = discord.Embed(color=discord.Color.random())
        em.add_field(name='Required Installations', value='**Python**\n[Download](https://python.org/downloads)\n**Discord.py**\nWindows\n`py -3 -m pip install -U discord.py`\nMac/Linux\n`python3 -m pip install -U discord.py`')
        await ctx.reply(embed=em, mention_author=False)


def setup(bot):
    bot.add_cog(Discord(bot))