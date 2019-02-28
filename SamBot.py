#Ted Clifford (c) 2.26.2019


import discord
import discordToken

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as {0.user}'.format(client))

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
    """
    Bot command function
    """
    #Bot will not respond to itself
    if message.author == client.user:
        return

    #Help message
    if message.content.startswith("$help"):
        await message.channel.send("""Hi, I'm SamBot
Prefix your commands with a '$'
Check out some of the cool things I can do!

1. Look pretty""")

    if message.content.startswith("$hello"):
        await message.channel.send("Hello {0.author.mention}".format(message))



client.run(discordToken.getToken())
