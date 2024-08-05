import discord
from discord.ext import commands
import requests
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

countrys = {
    'colombia': 239,
}


def get_football_matches_by_league(date, league_id, season):
    FOOTBALL_API_KEY = os.getenv('FOOTBALL_API_KEY')
    FOOTBALL_API_HOST = os.getenv('FOOTBALL_API_HOST')
    url = "https://api-football-v1.p.rapidapi.com/v3/fixtures"
    querystring = {
        "date": date,
        "league": league_id,
        "season": season
    }
    headers = {
        'x-rapidapi-key': FOOTBALL_API_KEY,
        'x-rapidapi-host': FOOTBALL_API_HOST
    }
    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        return response.json()
    else:
        return None


token = os.getenv('DISCORD_TOKEN')


intents = discord.Intents.all()
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix='-', intents=intents)


@bot.command()
async def info(ctx):
    await ctx.send('Soy un bot desarrollado para chimbear a Panda')


@bot.command()
async def partidos(ctx, country: str, season: int, date: str):
    league_id = countrys[country.lower()]
    matches = get_football_matches_by_league(date, league_id, season)
    if matches:
        response = ""
        for match in matches['response']:
            response += f"{match['teams']['home']['name']} vs {match['teams']
                                                               ['away']['name']} at {match['fixture']['date']}\n"
        await ctx.send(response)
    else:
        await ctx.send('No se encontraron partidos')


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'hola':
        await message.channel.send(f'Hola {message.author.name}')

    await bot.process_commands(message)

bot.run(token)
