import discord
from discord.ext import commands
import requests
import re
import os
from urllib.parse import urlencode
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

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


intents = discord.Intents.all()
intents.messages = True
intents.members = True

bot = commands.Bot(command_prefix='-', intents=intents)


@bot.command()
async def info(ctx):
    await ctx.send('Soy un bot desarrollado para chimbear a Panda')


@bot.command()
async def partidos(ctx, country: str, date: str):
    season = date.split('-')[0]
    league_id = countrys[country.lower()]
    matches = get_football_matches_by_league(date, league_id, season)
    if matches:
        response = ""
        for match in matches['response']:
            response += (f"{match['teams']['home']['name']} vs {match['teams']['away']['name']} - Resultado: "
                         f"{match['score']['fulltime']['home']} - {match['score']['fulltime']['away']}\n")
        await ctx.send(response)
    else:
        await ctx.send('No se encontraron partidos')


@bot.command()
async def youtube(ctx, *, search):
    base_url = 'https://www.youtube.com/results?'
    query_string = urlencode({'search_query': search})
    url = base_url + query_string
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3'}
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        await ctx.send('No se pudo realizar la busqueda')
    else:
        search_results = re.findall(
            '\\/watch\\?v=(.{11})', response.text)
        await ctx.send('https://www.youtube.com/watch?v=' + search_results[0])


@bot.event
async def on_message(message):
    if message.author == bot.user:
        return

    if message.content == 'hola':
        await message.channel.send(f'Hola {message.author.name}')

    await bot.process_commands(message)

bot.run(DISCORD_TOKEN)
