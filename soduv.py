import json
import discord
import asyncio
import decks
import random

with open("client_data.json", "r") as f:
    clientdata = json.load(f)


client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print(client.user.id)
    print('------')

@client.event
async def on_message(message):
    if message.content[:5].lower() == "soduv" or client.user.mention in message.content or isinstance(message.channel, discord.PrivateChannel) and not message.author.bot:
        if "rw" in message.content:
            deck = decks.RW_DECK
        elif "rune" in message.content:
            deck = decks.RUNES
        else:
            deck = decks.THOTH
        if "spread" in message.content:
            await client.send_message(message.channel, message.author.mention+" "+" ".join(random.sample(deck, 3)))
        else:
            await client.send_message(message.channel, message.author.mention+" "+random.choice(deck))

client.run(clientdata["token"])

