# todo
# adicionar canal que o bot vai ler as mensagens
# FEITO - adicionar o <user> disse: no começo do tts 
# adicionar comando de para limpar queue

# adicionar a API do is there any deal - https://docs.isthereanydeal.com/#tag/Prices/operation/games-overview-v2
# colocar essa funcionalidade em um comando

# fazer um sistema de rolagem de dados simples
# o valor do dado vai ser falado pelo bot de tts e dependendo do valor do dado vai ter falas especiais

# adicionar comando para o critterPedia pela API - https://www.postman.com/carson-hunter-team/acnh/api/448eae82-4ca9-41a5-a440-3bdb488171d4/documentation/1432573-3f69bc12-124b-48c0-aacf-c6121d11ff51?branch=&version=




import os 
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import requests
import asyncio
import ttsFile
import messageHandler


# get token
load_dotenv()
TOKEN = os.getenv("TOKEN")

# # list for queue tts
# TTS_QUEUE = []
# TTS_URL = "https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=pt&q="

# just default intents so the bot can work
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)
client = discord.Client(intents=intents)
tree = app_commands.CommandTree(client)

# set the Guild ID
# esse ID é do server do Gio
GUILD_ID = 1011350903221145737
target_guild = discord.Object(id=GUILD_ID)

# bot.event é para marcar um event handler
@bot.event
async def on_ready():
        try:
                comSync = await bot.tree.sync(guild=target_guild)
                print(f"sync: {len(comSync)} comms")
        except:
                print("not sync")


# bot.tree.command adiciona um slash command "/"
@bot.tree.command(
        name="config",
        description="configure the ttsBot",
        guild=target_guild
)
# abaixo do decorator vem a função que o slash command "/" vai chamar
async def config(ctx):
        await ctx.channel.send("arg")


@bot.tree.command(
        name="r_channel",
        description="select a channel to read the messages (the bot will only read from that channel)",
        guild=target_guild
)
async def channel_to_read(ctx):
        await ctx.channel.send("selecionando canal")

@bot.tree.command(
        name = "clear_tts",
        description="comando para limpar a fila de tts, caso o bot morra ou algo assim",
        guild=target_guild
)
async def clear_tts(ctx):
        ttsFile.TTS_QUEUE.clear()
        await ctx.channel.send("a fila de tts foi esvaziada")



@bot.event
async def on_message(msg):
        if msg.author.id != bot.user.id:
                await messageHandler.messageHandler(msg=msg, bot=bot)




bot.run(TOKEN)