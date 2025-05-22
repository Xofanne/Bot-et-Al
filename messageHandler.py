import os 
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import requests
import asyncio
import re
from random import randint
import ttsFile
import json




# regex simples para verificar se a pessoa chamou uma rolagem de dados
# ex:   "3d20" é uma chamada válida
#       "3d20 qualquer coisa depois na mensagem" não é uma chamada válida
roll_20_re = "^[0-9]+[d][0-9]+$"

# regex para verificar se o texto é um site
linkhttps = "https://"
linkhttp = "http://"


# toda mensagem deve passar por esse messageHandler e a partir daqui será definido
# qual a tratativa da mensagem
async def messageHandler(msg, bot):
        if re.search(roll_20_re, msg.content):
                await roll20(msg, bot)
        elif re.search(linkhttps, msg.content):
                await linkMsgHttps(msg, bot)
        elif re.search(linkhttp, msg.content):
                await linkMsgHttp(msg, bot)
        else:
                await ttsFile.buildTTS(tts_query=msg, bot=bot)


async def roll20(msg, bot):
        rolls = msg.content.split("d")
        total = 0
        texto = ""
        for tries in range(int(rolls[0])):
                atual = randint(1, int(rolls[1]))
                total += atual
                # await msg.channel.send(f"dado nº {tries+1} -> {atual}")
                texto += f"dado nº {tries+1} -> {atual}\n"
        msg.content = f"{msg.author.display_name} rolou {rolls[0]} d {rolls[1]} e tirou {total}"
        await msg.channel.send(texto + msg.content)
        await ttsFile.buildTTS(tts_query=msg, bot=bot)

async def linkMsgHttps(msg, bot):
        
        site = msg.content.replace("https://", ".https://.").split(".")

        if msg.content.find(" ", msg.content.find("https://")) == -1:
                link = msg.content[msg.content.find("https://")::]
        else:
                link = msg.content[msg.content.find("https://"):msg.content.find(" ", msg.content.find("https://"))+1:]


        if site[site.index("https://")+1] == "www" and msg.content.find(" "):
                msg.content = msg.content.replace(link, f"link {site[site.index("https://")+2]} ")
        elif site[site.index("https://")+1] == "www" and not msg.content.find(" "):
                msg.content = msg.content.replace(link, f"link {site[site.index("https://")+2]} ")
        elif site[site.index("https://")+1] != "www" and msg.content.find(" "):
                msg.content = msg.content.replace(link, f"link {site[site.index("https://")+1]} ")
        else:
                msg.content = msg.content.replace(link, f"link {site[site.index("https://")+1]} ")
        await ttsFile.buildTTS(tts_query=msg, bot=bot)

async def linkMsgHttp(msg, bot):

        if msg.content.find(" ", msg.content.find("http://")) == -1:
                link = msg.content[msg.content.find("http://")::]
        else:
                link = msg.content[msg.content.find("http://"):msg.content.find(" ", msg.content.find("http://"))+1:]

        site = msg.content.replace("http://", ".http://.").split(".")

        if site[site.index("http://")+1] == "www" and msg.content.find(" "):
                msg.content = msg.content.replace(link, f"link {site[site.index("http://")+2]} ")
        elif site[site.index("http://")+1] == "www" and not msg.content.find(" "):
                msg.content = msg.content.replace(link, f"link {site[site.index("http://")+2]} ")
        elif site[site.index("http://")+1] != "www" and msg.content.find(" "):
                msg.content = msg.content.replace(link, f"link {site[site.index("http://")+1]} ")
        else:
                msg.content = msg.content.replace(link, f"link {site[site.index("http://")+1]} ")
        await ttsFile.buildTTS(tts_query=msg, bot=bot)