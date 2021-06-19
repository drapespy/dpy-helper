import discord
from discord.ext import commands

import asyncio, aiohttp




class Discord(commands.Cog):
    def __init__(self,bot):
        self.bot = bot
        self.session = aiohttp.ClientSession()

    async def refer(self, ctx:commands.Context, **kwargs):
        """
        Replying to the message reference
        """
        if ctx.message.reference:
            channel = self.bot.get_channel(ctx.message.reference.channel_id)
            msg = await channel.fetch_message(ctx.message.reference.message_id)
            return await msg.reply(**kwargs)

        else:
            return await ctx.message.reply(mention_author=False, **kwargs)

    # api finder command
    @commands.command(hidden=True)
    async def find(self,ctx):

        await ctx.reply(f"This command has been deprecated. Use `?rtfm` instead.", mention_author=False)
    
    @commands.command()
    async def pypi(self, ctx, name):
        async with self.session.get(f"https://pypi.org/pypi/{name}/json") as resp:
            if resp.status == 404:
                return await ctx.send(f"Unable to find package: *{name}*")
            package = await resp.json()
            package = package["info"]
            Author = f"""
            **Author:** {package.get('author') or "None"}
            **Author email:** {package["author_email"] or "None"}
            """
            Package = f"""
            **Homepage:** {package.get("home_page") or "None"}
            **License:** {package.get("license") or "None"}
            **Version:** {package.get("version") or "None"}
            **Keywords:** {package.get("keywords") or "None"}
            **Documentation:** {package.get("project_urls").get("Documentation") or "None"}
            """
            embed = discord.Embed(
                color=discord.Color.random(),
                title=package["name"],
                url=package["package_url"],
                description=package["summary"],
            )
            embed.set_thumbnail(url="https://i.imgur.com/8EI9rk0.png")
            embed.add_field(name="Package", value=Package, inline=False)
            embed.add_field(name="Author", value=Author, inline=False)
            await self.refer(ctx, embed=embed)

    @commands.command()
    async def tags(self, ctx):
        await ctx.send(embed=discord.Embed(description='**List of tags:**\n`status`\n`activity`\n`code`\n`type`\n`music`\n\nUse `?tag <tag>` to view the tag', color=discord.Color.random()))

    @commands.group(invoke_without_command=True, hidden=True)
    async def tag(self, ctx):
        await ctx.send('Please provided a tag!\nUse `?tags` for a list of tags')
            

    @tag.command()
    async def status(self, ctx):
        msg = '<:s_Online:827276470148923392> <:s_Idle:827276518551977984> <:s_Dnd:827276569680543844> <:s_Invis:827276650336747520>\n```py\n# Online\nawait bot.change_presence(status=discord.Status.online)\n\n# Idle\nawait bot.change_presence(status=discord.Status.idle)\n\n# Do Not Disturb\nawait bot.change_presence(status=discord.Status.dnd)\n\n# Invisible\nawait bot.change_presence(status=discord.Status.offline)\n```'
        await self.refer(ctx, content=msg)

    @tag.command(aliases=['presence', 'rp', 'rich_presence'])
    async def activity(self, ctx):
        await self.refer(ctx, content='```py\n# Playing\nawait bot.change_presence(activity=discord.Game(name="a game"))\n\n# Streaming\nawait bot.change_presence(activity=discord.Streaming(name="My Stream", url="https://twitch.tv/settings"))\n\n# Listening\nawait bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="a song"))\n\n# Watching\nawait bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="a movie"))\n\n# Competing\nawait bot.change_presence(activity=discord.Activity(type=discord.ActivityType.competing, name="eSports"))\n```')

    # code blocks command
    @tag.command(aliases=['codeblocks','blocks'])
    async def code(self,ctx):
        em = discord.Embed(
            title = 'Using code blocks in python. \nHere\'s how to format Python code on Discord:',
            description = "**Input:**\n\```py\nprint('Hello world!')\n\```\n**Output:**\n```py\nprint('Hello world')```\n\nThese are backticks, not quotes. Check [this](https://superuser.com/questions/254076/how-do-i-type-the-tick-and-backtick-characters-on-windows/254077#254077) out if you can't find the backtick key.",
            color = discord.Color.random()
        )
        await self.refer(ctx, embed=em)
    
    # How to type
    @tag.command()
    async def type(self,ctx):
        async with ctx.typing():
            await asyncio.sleep(1.5)
        await self.refer(ctx, content="<a:type:826891270634340384> **Discord.py helper** is typing...\n```py\nimport asyncio\n\n@bot.command()\nasync def command_name(ctx):\n    async with ctx.typing():\n        # Do stuff here\n        await asyncio.sleep(x)\n    await ctx.send('Message here.')\n```")

    @tag.command()
    async def music(self,ctx):
        await self.refer(ctx, content='Want to make an easy Music bot?\nThen DiscordUtils is the perfect thing for you.\nDocs: <https://docs.discordutils.gq/music>\nGithub: <https://github.com/toxicrecker/DiscordUtils>\n\nWant something more complicated but better in the long run? Then check out **wavelink**\nDocs: <https://wavelink.readthedocs.io/en/latest/wavelink.html#>\nGithub: <https://github.com/PythonistaGuild/Wavelink>')

    # links command 
    @commands.command()
    async def links(self,ctx):
        em = discord.Embed(color=discord.Color.random())
        em.add_field(name='Required Installations', value='**Python**\n[Download](https://python.org/downloads)\n**Discord.py**\nWindows\n`py -3 -m pip install -U discord.py`\nMac/Linux\n`python3 -m pip install -U discord.py`')
        await ctx.reply(embed=em, mention_author=False)


def setup(bot):
    bot.add_cog(Discord(bot))