import json
import discord
import asyncio

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
    if message.content.startswith('Soduv') or client.user.mention in message.content:
        await client.send_message(message.channel, message.author.mention+" pong")

client.run(clientdata["token"])

