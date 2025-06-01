import requests
import json
import sys
import datetime
import discord
from pagination import Pagination
from dotenv import load_dotenv
import os

URL = 'https://api.nookipedia.com/'

load_dotenv()
API_KEY = os.getenv("ACAPI")

HEADER = {
        "X-API-KEY": API_KEY,
        "Accept_Version": "1.0.0"}

LETTERS = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"

async def list_villager(name: str, embed):
        url = f"{URL}villagers"

        params = {"name":name.title(), "game":"NH", "nhdetails":"true"}

        response = requests.get(url, headers=HEADER, params=params)
        response_json = response.json()


        final_string = f"# {name.title()}\n- **Birthday**: {response_json[0]["birthday_day"]} - {response_json[0]["birthday_month"]}\n - **Personality**: {response_json[0]["personality"]}\n- **Hobby**: {response_json[0]["nh_details"]["hobby"]}"

        embed.set_image(url=response_json[0]["nh_details"]["photo_url"])
        embed.description = final_string

        return embed

async def list_bug(name: str, embed):
        url = f"{URL}nh/bugs/{name.lower()}"

        response = requests.get(url, headers=HEADER, params={"thumbsize":256})
        response_json = response.json()

        final_string = f"# {name.title()}\n- **Location**: {response_json['location']}\n- **Wheather**: {response_json['weather']}\n- **Months**: {response_json['south']['availability_array'][0]['months']}\n- **Time**: {response_json['south']['availability_array'][0]['time']}"

        embed.set_image(url = response_json["render_url"])
        embed.description = final_string

        return embed

async def list_fish(name, embed):
        url = f"{URL}nh/fish/{name.lower()}"

        response = requests.get(url, headers=HEADER, params={"thumbsize":256})
        response_json = response.json()

        final_string = f"# {name.title()}\n- **Local :** {response_json["location"]}\n- **Tamanho da sombra :** {response_json["shadow_size"]}\n- **Disponibilidade :**\n"

        for x in response_json["south"]["availability_array"]:
                final_string += f"{x["months"]} - {x["time"]}\n"

        embed.set_image(url=response_json["render_url"])
        embed.description = final_string

        return embed

async def list_all(type: str, month=""):
        params = {
                "month":month,
                "excludedetails":'true'     
        } if month != "" else {"excludedetails":'true'}

        url = f"{URL}nh/{type}"

        response = requests.get(url, headers=HEADER, params=params)
        response_json = response.json()

        match type:
                case "bugs":
                        creature = "Bugs"
                case "fish":
                        creature = "Fish"
                case "sea":
                        creature = "Sea Creatures"

        things_per_letter: dict[str:list] = {x:[] for (x) in LETTERS}

        if month != "":
                final_string = f"# All {creature} of {month}\n"
                for x in response_json["south"]:
                        if not things_per_letter[x[0].upper()]:
                                things_per_letter[x[0].upper()] = [x.title()]
                        else:
                                things_per_letter[x[0].upper()].append(x.title())
        else:
                final_string = f"# All {creature}\n"
                for x in response_json:
                        if not things_per_letter[x[0].upper()]:
                                things_per_letter[x[0].upper()] = [x.title()]
                        else:
                                things_per_letter[x[0].upper()].append(x.title())

        for x in LETTERS:
                if things_per_letter[x] != []:
                        final_string += f"### {x} :\n"
                        for v in things_per_letter[x]:
                                final_string += f"- {v}\n"


        if response.status_code == 200:
                return final_string
        return response.status_code 