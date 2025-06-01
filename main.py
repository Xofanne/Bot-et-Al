# todo
# adicionar canal que o bot vai ler as mensagens
# FEITO - adicionar o <user> disse: no começo do tts 
# adicionar comando de para limpar queue

# adicionar a API do is there any deal - https://docs.isthereanydeal.com/#tag/Prices/operation/games-overview-v2
# colocar essa funcionalidade em um comando

# fazer um sistema de rolagem de dados simples
# o valor do dado vai ser falado pelo bot de tts e dependendo do valor do dado vai ter falas especiais

# adicionar comando para o critterPedia pela API - https://www.postman.com/carson-hunter-team/acnh/api/448eae82-4ca9-41a5-a440-3bdb488171d4/documentation/1432573-3f69bc12-124b-48c0-aacf-c6121d11ff51?branch=&version=



        ## FAZER UMA FUNÇÃO PARA ALTERAR O ARQUIVO JSON E O ARQUIVO TXT UMA UNICA VEZ E A PARTIR DESSA CHAMADA ALTERAR UMA LISTA DE CONFIG RODANDO EM MEMÓRIA



import os 
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import requests
import asyncio
import ttsFile
import messageHandler
import json
import AC_API


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

# # AL el AL
# GUILD_ID = 338133173533671425

target_guild = [discord.Object(id=1011350903221145737), discord.Object(id=338133173533671425)]

# bot.event é para marcar um event handler
@bot.event
async def on_ready():
        for id in target_guild:
                try:
                        comSync = await bot.tree.sync(guild=id)
                        print(f"sync: {len(comSync)} comms in guild {id}")
                except:
                        print("not sync")


# bot.tree.command adiciona um slash command "/"
@bot.tree.command(
        name="config",
        description="configure the ttsBot",
        guilds=target_guild
)
# abaixo do decorator vem a função que o slash command "/" vai chamar
async def config(ctx):
        await ctx.channel.send("arg")


##### TTS COMMANDS

@bot.tree.command(
        name="set_channel",
        description="select a channel to read the messages (the bot will only read from that channel)",
        guilds=target_guild,
)
async def channel_to_read(ctx):
        channel_ID = ctx.channel_id
        print(channel_ID)
        with open("channels.json", 'r') as file:
                channels_load = json.load(file)
        print(channels_load)
        channels_load["channels"].append(channel_ID)
        print(channels_load)
        with open("channels.json", "w") as file:
                json.dump(channels_load, file)


@bot.tree.command(
        name = "clear_tts",
        description="comando para limpar a fila de tts, caso o bot morra ou algo assim",
        guilds=target_guild
)
async def clear_tts(ctx):
        ttsFile.TTS_QUEUE.clear()
        await ctx.channel.send("a fila de tts foi esvaziada")



##### AC COMMANDS

@bot.tree.command(
                name="ac_bugs_list",
                description="retorna o nome de todos os insetos do Animal Crossing NH",
                guilds=target_guild
)
async def list_all_bugs(ctx, month: str = ""):
        await ctx.channel.send( await AC_API.list_all("bugs", month))


@bot.tree.command(
                name="ac_bug",
                description="retorna dados sobre um inseto específico",
                guilds=target_guild
)
async def list_bug(ctx, name: str = ""):
        await ctx.channel.send( embed = await AC_API.list_bug(name, embed=discord.Embed()))


@bot.tree.command(
                name="ac_fish_list",
                description="retorna o nome de todos os peixes do Animal Crossing NH",
                guilds=target_guild
)
async def list_all_fish(ctx, month: str = ""):
        await ctx.channel.send(await AC_API.list_all("fish", month))

@bot.tree.command(
                name="ac_sea_list",
                description="retorna o nome de todas as criaturas marinhas do Animal Crossing NH",
                guilds=target_guild
)
async def list_all_sea_creatures(ctx, month: str = ""):
        await ctx.channel.send(await AC_API.list_all("sea", month))


@bot.tree.command(
                name="ac_fish",
                description="retorna informações sobre um peixe específico",
                guilds=target_guild
)
async def lisf_fish(ctx, name: str =""):
        await ctx.channel.send( embed = await AC_API.list_fish(name, embed = discord.Embed()))


@bot.tree.command(
                name="ac_villager",
                description="return picture, birthday and personality of a villager",
                guilds=target_guild
)
async def list_villager(ctx, name:str = ""):
        await ctx.channel.send(embed = await AC_API.list_villager(name, embed=discord.Embed()))



@bot.event
async def on_message(msg):

        if msg.author.id == bot.user.id:
                return
        
        with open("channels.json", "r") as file:
                x = json.load(file)
        if msg.channel.id in x["channels"]:
                await messageHandler.messageHandler(msg=msg, bot=bot)
                return
        return


bot.run(TOKEN)