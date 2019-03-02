#Ted Clifford (c) 2.26.2019

import discord, discordToken
import aiohttp

from urllib import parse
from discord.ext import commands

BOT_PREFIX = "$"
start_message = True

# TODO Stocks, ?dow ?nyse cvs
# TODO ?stats - # messages, number of new joins over time (Generate image and upload?)
# TODO add "Roll" for dice roll
# TODO Weather?
# TODO Define?
# TODO fortune cookie
# TODO !remind me
# TODO On ready announce to server or to channel - I'm here to help!
# TODO news or feed command

client = commands.Bot(command_prefix = BOT_PREFIX)
print("Starting...")

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))
    await client.change_presence(game = discord.Game(name = "with your hearts"))

    if start_message:
        for server in client.servers:
            for channel in server.channels:
                if channel.permissions_for(server.me).send_messages:
                    try:
                        await client.send_message(channel, "SamBot online, ready to go! Type $help to see what I can do.")
                        break
                    except:
                        continue

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
    category = "Commands",
    pass_context = True)
async def bitcoin(context):
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:
        raw_response = await session.get(url)
        response = await raw_response.json()
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

@client.command(description = "Prints a test message.",
    brief = "Bot test",
    alias = ["t"],
    category = "Commands",
    pass_context = True)
async def test(context, *args):
    await client.say("Hello world, {}".format(context.message.author.mention) + "\nYou passed: {}".format(", ".join(args)))

@client.command(description = "Prints out information about the bot and it's creator.",
    brief = "Display bot information",
    alias = ["i"],
    category = "Commands",
    pass_context = True)
async def info(context):
    await client.say("""Hi, I'm SamBot
Prefix your commands with a '$'
Check out some of the cool things I can do!

1. Look pretty
2. Be an Absolute UNIT
""")

client.run(discordToken.getToken())
