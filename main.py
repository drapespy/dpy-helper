import discord
from discord.ext import commands, tasks
from keep_alive import keep_alive
import os
import asyncio, aiohttp, traceback, time

# Embed
class Help(commands.MinimalHelpCommand):
    async def send_pages(self):
        destination = self.get_destination()
        for page in self.paginator.pages:
            emby = discord.Embed(description=page, color=discord.Color.random())
            await destination.send(embed=emby)

# intents and prefix
class Bot(commands.AutoShardedBot):
    def __init__(self, **kwargs):
        super().__init__(
            command_prefix='?',
            intents=discord.Intents.all(),
            help_command=commands.MinimalHelpCommand(sort_commands=False),
            **kwargs
            )
        
        self.session = self._session()

    async def _session(self):
        """Aiohttp Session"""
        return aiohttp.ClientSession()

    

bot = Bot()
bot.load_extension('jishaku')
os.environ['JISHAKU_HIDE'] = 'True'
os.environ['JISHAKU_NO_UNDERSCORE'] = 'True'
os.environ['JISHAKU_NO_DM_TRACEBACK'] = 'True'

# on_ready event
@bot.event
async def on_ready():
    ch_pr.start()
    print('Bot ready!')

@tasks.loop(seconds=90.0)
async def ch_pr():
    await bot.change_presence(status=discord.Status.dnd, activity=discord.Activity(type=discord.ActivityType.competing, name="?help"))

# command error handler

@bot.event
async def on_command_error(ctx, error):
    error = getattr(error, 'original', error)
    if isinstance(error, commands.CommandNotFound):
        """
        Crickets...
        """
    elif isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(f'{error.param.name} is a required argument that is missing.')
    else:
        await ctx.send("```py\n" + "".join(traceback.format_exception(error, error, error.__traceback__)) + "\n```")

# shutdown command
@bot.command(aliases=['shut','shutdown'], hidden=True)
@commands.is_owner()
async def logout(ctx):
    await ctx.send('Shutting down...')
    await ctx.message.add_reaction('<:dpy:822525536450510868>')
    await bot.close() 

@bot.command(description='Bot latency')
async def ping(ctx):
    tstart = time.perf_counter()
    await ctx.trigger_typing()
    tend = time.perf_counter()
    tlatency = round((tend - tstart) * 1000, 2)
    mstart = time.perf_counter()
    msg = await ctx.send('Pinging...')
    mend = time.perf_counter()
    mlatency = round((mend - mstart) * 1000, 2)
    estart = time.perf_counter()
    await msg.edit(content='Pong!')
    eend = time.perf_counter()
    elatency = round((eend - estart) * 1000, 2)
    web = round(bot.latency * 1000, 2)
    dstart = time.perf_counter()
    await msg.delete()
    dend = time.perf_counter()
    dlatency = round((dend - dstart) * 1000, 2)
    _embed = discord.Embed(
        title = ':ping_pong: Pong!', 
        description = f'**Recieval latency:** {web} ms\n'
        f'**Typing latency:** {tlatency} ms\n'
        f'**Message latency:** {mlatency} ms\n'
        f'**Edit latency:** {elatency} ms\n'
        f'**Delete latency:** {dlatency} ms',
        color=discord.Color.green()
    )
    await ctx.send(embed=_embed)



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