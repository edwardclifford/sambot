#Ted Clifford (c) 2.26.2019

import discord, discordToken
import aiohttp

from urllib import parse
from discord.ext import commands

BOT_PREFIX = "$"
start_message = False    #Set false when testing

# TODO ?stats - # messages, number of new joins over time (Generate image and upload?)
# TODO add "Roll" for dice roll
# TODO Weather?
# TODO Define?
# TODO fortune cookie
# TODO !remind me
# TODO news or feed command
# TODO let me google that for you (lmgtfy)
# TODO poll tally function

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

@client.command(description = "Creates a poll based on a question and up to 10 options.",
    brief = "Create a poll",
    alias = ["p"],
    pass_context = True)
async def poll(context, question, *options: str):
    if len(options) <= 1:
        await client.say("You must enter more than one option.")
        return
    elif len(options) > 10:
        await client.say("You cannot enter more than 10 options.")
        return

    if len(options) == 2 and options[0] == 'yes' and options[1] == 'no':
        reactions = ['✅', '❌']
    else:
        reactions = ['1⃣', '2⃣', '3⃣', '4⃣', '5⃣', '6⃣', '7⃣', '8⃣', '9⃣', '🔟']

    description = []
    for x, option in enumerate(options):
        description += '\n {} {}'.format(reactions[x], option)

    embed = discord.Embed(title=question, description=''.join(description))
    react_message = await client.say(embed=embed)

    for reaction in reactions[:len(options)]:
        await client.add_reaction(react_message, reaction)

    # embed.set_footer(text='Poll ID: {}'.format(react_message.id))   For whenever you want to add a tally function
    await client.edit_message(react_message, embed=embed)

@client.command(description = "Checks the current market price for the stock requested.",
    brief = "Get price for a share",
    aliases = ["stock"],
    pass_context = True)
async def price(context, symbol):
    url = 'https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=' + symbol + '&interval=5min&apikey=00VKIV627UD97WIE'
    async with aiohttp.ClientSession() as session:
        raw_response = await session.get(url)
        response = await raw_response.json()
        if response:
            await client.say("Current stock price of " + symbol + ": " + response["Time Series (5min)"][list(response[list(response.keys())[1]].keys())[0]]["4. close"])
        else:
            await client.say("I couldn't find a stock price for that symbol :/")

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
    alias = ["t"],
    pass_context = True)
async def test(context, *args):
    await client.say("Hello world, {}".format(context.message.author.mention) + "\nYou passed: {}".format(", ".join(args)))

@client.command(description = "Prints out information about the bot and it's creator.",
    brief = "Display bot information",
    alias = ["i"],
    pass_context = True)
async def info(context):
    await client.say("""Hi, I'm SamBot
Prefix your commands with a '$'
Check out some of the cool things I can do!

1. Look pretty
2. Be an Absolute UNIT
""")

client.run(discordToken.getToken())
