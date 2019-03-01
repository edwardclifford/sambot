#Ted Clifford (c) 2.26.2019

import discord
import discordToken
import aiohttp

from urllib import parse
from discord.ext.commands import Bot

BOT_PREFIX = "$"

# TODO Stocks, ?dow ?nyse cvs
# TODO ?stats - # messages, number of new joins over time (Generate image and upload?)
# TODO add "Roll" for dice roll
# TODO Weather?
# TODO Define?
# TODO fortune cookie
# TODO !remind me
# TODO On ready announce to server or to channel - I'm here to help! Just type ?help in the #help-desk channel.
# TODO news or feed command

client = Bot(command_prefix = BOT_PREFIX)
print("Starting...")

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(game = discord.Game(name = "SamBot"))

@client.event
async def on_member_join(member):
    """
    Welcome message for new members joining the server
    """
    server = member.server
    fmt = "Welcome {0.name} to {1.server}!"
    await client.send_message(server, fmt.format(member, server))

@client.event
async def on_message(message):
    #The bot should not reply to itself
    if message.author == client.user:
        return

    if message.content.startswith(BOT_PREFIX):
        await client.process_commands(message)

@client.command(description = "Checks the current Bitcoin price in US Dollars from Coinbase.",
    brief = "Get current Bitcoin price",
    aliases = ["btc"],
    pass_context = True)
async def bitcoin(context):
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:
        raw_response = await session.get(url)
        response = await raw_response.json()
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

@client.command(description = "Prints a test message.",
    brief = "Bot test",
    alias = ["test"],
    pass_context = True)
async def test(context, *args):
    await client.say("Hello world, {0.author.message}".format(context.author),
        "You passed: {}".format(", ".join(args)))

@client.command(description = "Prints out the help message,",
    brief = "Help message",
    alias = ['h', "?"],
    pass_context = True)
async def test(context):
    await client.say("""Hi, I'm SamBot
Prefix your commands with a '$'
Check out some of the cool things I can do!

1. Look pretty
2. Be an Absolute UNIT
""")

client.run(discordToken.getToken())
