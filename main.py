from discord.ext import commands, tasks
import requests
from bs4 import BeautifulSoup
from datetime import date
# import asyncio
# while not used currently this is needed for setting what time you want the getWordOnceADay function to go
import os
from dotenv import load_dotenv

load_dotenv()  # Used to make it so os.getenv can get the token from the .env file
bot = commands.Bot(command_prefix='!')


@bot.event
async def on_ready():
    print("The bot is ready!")


@bot.command()
async def hello(ctx):
    await ctx.send("Hello!")


# TODO: Can I add a command event that lets users pull up the daily word? Limit how many calls

@tasks.loop(hours=24)
async def getWordOnceADay():
    """Once a day getWordOnceADay gets the html from verterbukh's word of the day page with requests.
    It then separates the html into printable strings with BeautifulSoup. It will eventually post
    this information formatted in the designated channel"""
    message_channel = bot.get_channel(818037105900650510)

    URL = 'https://verterbukh.org/vb?page=wdmin'
    page = requests.get(URL)

    soup = BeautifulSoup(page.content, 'html.parser')

    # TODO:Prettify the data in dayword. Maybe split it like gen?

    dayWord = soup.find("span", class_="lemma")

    gend = soup.find("span", class_="glossed")

    defined = soup.find("div", class_="gloss")  # Maybe this should be a find_all so I can get a variable amount of def.

    # TODO: Get it to iterate through all the different gloss terms + additional yiddish. Maybe for string in x?

    articleInYiddish = gend.find_next(string=True)
    await  message_channel.send(defined)
    await message_channel.send("----" + str(date.today()) + "----")
    await message_channel.send(
        "**Word of the Day:** \n" + dayWord.text + "\n" + gend.span.string + " " + articleInYiddish + "\n" + defined.text)
    # TODO: Should I add what each line is for clarity?


@getWordOnceADay.before_loop
async def before_msg1():  # In order to calculate when the first message should be sent add
    # 'await asyncio.sleep([time here])'
    await bot.wait_until_ready()


getWordOnceADay.start()
bot.run(os.getenv('TOKEN'))  # Don't reveal your bot token, regenerate it asap if you do
