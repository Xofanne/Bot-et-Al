import os 
import discord
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv
import requests
import asyncio


# links são falados por extenso
# https://tenor.com/view/elmo-burning-burn-hell-red-gif-10327579165149556602
# https://www.youtube.com/watch?v=4haAdmHqGOw

# não falados - []{}ºª?!§&()+-()\# 


# list for queue tts
TTS_QUEUE = []
TTS_URL = "https://translate.google.com/translate_tts?ie=UTF-8&client=tw-ob&tl=pt&q="

async def botConnect(tts, bot):
        
        # aparentemente isso aqui define qual voice channel o bot está conectado
        voice_client = discord.utils.get(bot.voice_clients, guild=tts.guild)
        if voice_client != None:
                return voice_client
        else:
                voice_channel = tts.author.voice

                if voice_channel is None:
                        return 2
                

                # seleciona o canal ativo de quem chamou o comando e conecta o bot
                if voice_client is None:
                        voice_client = await voice_channel.channel.connect()
                elif voice_channel != voice_client.channel:
                        await voice_client.move_to(voice_channel.channel)
                
                return voice_client

async def buildTTS(tts_query, bot):
        
        # define o voice channel que a pessoa que digitou está
        # voice_channel = tts_query.author.voice

        ## TO DO acho que o nickname tem que ser definido dentro da chamada da outra
        ## função se não pode dar erro ao ter mais de uma pessoa digitando

        # define o nick do server e define quem foi o ultimo a digitar
        nickname = tts_query.author.display_name


        # # checa se o usuário que chamou o comando está em um canal de voz
        # if voice_channel is None:
        #         await tts_query.channel.send("você precisa estar em um canal de voz.")
        #         return
        
        # # aparentemente isso aqui define qual voice channel o bot está conectado
        # voice_client = tts_query.author.guild.voice_client

        # # seleciona o canal ativo de quem chamou o comando e conecta o bot
        # if voice_client is None:
        #         voice_client = await voice_channel.channel.connect()
        # elif voice_channel != voice_client.channel:
        #         await voice_client.move_to(voice_channel.channel)

        voice_client = await botConnect(tts_query, bot) if await botConnect(tts_query, bot) != 2 else 0
        if voice_client == 0:
                await tts_query.channel.send("você precisa estar em um canal de voz.")
                return

        # Set guild_id
        guild_id = str(tts_query.guild.id)


        # checar se a ultima pessoa que digitou e a que digitou agora são a mesma pessoa
        # se for diferente o bot vai falar o nick da pessoa
        # if nickname != last_spoke[0]:
        #         URL = f"{TTS_URL}{nickname}+disse: {tts_query.content.replace(' ', '+')}"
        # else:
        #         URL = TTS_URL + tts_query.content.replace(' ', '+')
        # last_person[0] = nickname
        URL = TTS_URL + tts_query.content.replace(' ', '+')

        # cada vez que o comando for chamado, adiciona a msg numa queue
        # if tts_query.author.display_name in TTS_QUEUE.keys():
        #         TTS_QUEUE[tts_query.author.display_name].append(URL)
        # else:
        #         TTS_QUEUE[tts_query.author.display_name] = [URL]
        TTS_QUEUE.append([nickname, f"{tts_query.content.replace(' ', '+')}"])

        # o comando só vai ser chamado aqui se não tiver tocando nenhum audio ou se um audio não estiver pausado
        if not voice_client.is_playing() and not voice_client.is_paused():
                # await queue_tts(nickname, voice_client, guild_id, tts_query.channel, bot=bot)
                await queue_tts(nickname, voice_client, bot=bot)

# async def queue_tts(nickname, voice_client, guild_id, channel, bot):
async def queue_tts(nickname, voice_client, bot):

        last = open("last.txt", "r").readline()
        # se existir uma mensagem na fila entra no código
        # if len(TTS_QUEUE[nickname]) != 0:
        if len(TTS_QUEUE) != 0:
                # tira a mensagem mais antiga da fila
                # tts_line = TTS_QUEUE[nickname].pop(0)
                tts_atual = TTS_QUEUE.pop(0)


                if tts_atual[0] != last:
                        tts_line = f"{TTS_URL}{tts_atual[0]}+disse: +{tts_atual[1]}"
                        with open("last.txt", "w") as l:
                                l.write(f"{tts_atual[0]}")
                else:
                        tts_line = f"{TTS_URL}{tts_atual[1]}"

                # config do ffmpeg
                ffmpeg_options = {
                        "before_options": "-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5",
                        "options": "-vn -c:a libopus -b:a 96k"
                }

                # cria o audio pra ser tocado
                source = discord.FFmpegOpusAudio(tts_line, **ffmpeg_options, executable="bin\\ffmpeg\\ffmpeg.exe")

                # define uma chamada recursiva para limpar a fila do tts
                def after_play(error):
                        if error:
                                print(f"erro ao reproduzir: {error}")
                        # esse asyncio vai rodar em loop a fila de tts até ela zerar
                        # asyncio.run_coroutine_threadsafe(queue_tts(nickname, voice_client, guild_id, channel, bot=bot), bot.loop)
                        asyncio.run_coroutine_threadsafe(queue_tts(nickname, voice_client, bot=bot), bot.loop)

                # toca o audio criado, o parametro after, chama a função after_play()
                # que vai limpando a lista de tts até não ter mais fila
                
                # a função queue_tts() só é chamada quando não tem fila de mensagens
                # caso tenha fila, a mensagem vai para a lista TTS_QUEUE que é esvaziada
                # nas chamadas recursivas dentro da função after_play()
                voice_client.play(source, after=after_play)