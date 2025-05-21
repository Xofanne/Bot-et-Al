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

# regex simples para verificar se a pessoa chamou uma rolagem de dados
# ex:   "3d20" é uma chamada válida
#       "3d20 qualquer coisa depois na mensagem" não é uma chamada válida
roll_20_re = "^[0-9]+[d][0-9]+$"

# toda mensagem deve passar por esse messageHandler e a partir daqui será definido
# qual a tratativa da mensagem
async def messageHandler(msg, bot):
        if re.search(roll_20_re, msg.content):
                await roll20(msg, bot)
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