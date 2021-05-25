import discord
from discord.ext import commands, tasks
from keep_alive import keep_alive
import os
import asyncio

class NewHelpName(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, color=discord.Color.random())
            await destination.send(embed=emby)

# intents and prefix
intents = discord.Intents.all()
bot = commands.Bot(command_prefix='?', intents=intents, help_command=NewHelpName())

# on_ready event
@bot.event
async def on_ready():
    ch_pr.start()
    print('Bot ready!')

@tasks.loop(seconds=90.0)
async def ch_pr():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.competing, name="?help"))



# command error handler

# shutdown command
@bot.command(aliases=['shut','shutdown'], hidden=True)
@commands.is_owner()
async def logout(ctx):
    await ctx.send('Shutting down...')
    await ctx.message.add_reaction('<:dpy:822525536450510868>')
    await bot.close() 

@bot.command(description='Bot latency')
async def ping(ctx):
    await ctx.reply(f'My latency is `{round(bot.latency * 1000)}`m/s', mention_author=False)

# COGS
@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, extension):
  bot.load_extension(f"cogs.{extension}")

@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, extension):
  bot.unload_extension(f"cogs.{extension}")

for filename in os.listdir('./cogs'):
  if filename.endswith('.py'):
    bot.load_extension(f"cogs.{filename[:-3]}")

# running then bot
keep_alive()
bot.run(os.getenv('TOKEN'))