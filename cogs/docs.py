import discord
from discord.ext import commands
from doc_search import AsyncScraper

scraper = AsyncScraper()

class Docs(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def refer(self, ctx:commands.Context, **kwargs):
        """
        Replying to the message reference
        """
        if ctx.message.reference:
            channel = self.bot.get_channel(ctx.message.reference.channel_id)
            msg = await channel.fetch_message(ctx.message.reference.message_id)
            return await msg.reply(mention_author=False, **kwargs)

        else:
            return await ctx.message.reply(mention_author=False, **kwargs)

    @commands.group(name='rtfm',aliases=['rtfd'], invoke_without_command=True)
    async def rtfm(self, ctx, *, query=None):
        """
        Documentation search command.
        The default is the discord.py documentation at https://discordpy.readthedocs.io/en/latest
        All other functionality is within its subcommands.
        """
        if not query:
            await self.refer(ctx, content='https://discordpy.readthedocs.io/en/latest')
        else:
            results = await scraper.search(query, page="https://discordpy.readthedocs.io/en/latest")
            if not results:
                await ctx.send("Could not find anything. Sorry.")
            else: 
                x = '\n'.join(['[`{}`]({})'.format(item.replace('discord.ext.commands.', '').replace('discord.', ''), url) for item, url in results[:8]])
                await self.refer(ctx, embed=discord.Embed(description=x, color=discord.Color.blurple()))

    @rtfm.command(name='python',aliases=['py'])
    async def rtfm_python(self, ctx, *, query=None):
        """
        Searches the official Python documentation at https://docs.python.org/3/
        """
        if not query:
            await self.refer(ctx, content='https://docs.python.org/3/')
        else:
            results = await scraper.search(query, page="https://docs.python.org/3/")
            if not results:
                await ctx.send("Could not find anything. Sorry.")
            else: 
                x = '\n'.join(['[`{}`]({})'.format(item, url) for item, url in results[:8]])
                await self.refer(ctx, embed=discord.Embed(description=x, color=discord.Color.blurple()))

    @rtfm.command(name='jishaku',aliases=['jsk'])
    async def rtfm_jishaku(self, ctx, *, query=None):
        """
        Searches the jishaku documentation at https://jishaku.readthedocs.io/en/latest/
        """
        if not query:
            await self.refer(ctx, content='https://jishaku.readthedocs.io/en/latest/')
        else:
            results = await scraper.search(query, page="https://jishaku.readthedocs.io/en/latest/")
            if not results:
                await ctx.send("Could not find anything. Sorry.")
            else: 
                x = '\n'.join(['[`{}`]({})'.format(item, url) for item, url in results[:8]])
                await self.refer(ctx, embed=discord.Embed(description=x, color=discord.Color.blurple()))

def setup(bot):
    bot.add_cog(Docs(bot))
