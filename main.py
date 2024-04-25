import discord
import os
import requests
import json
import pandas as pd
import random
from dotenv import load_dotenv


intents = discord.Intents()
intents.messages=True
intents.message_content=True
client = discord.Client(intents=intents)
words = ["funny", "laugh"]

def get_joke():
    response = requests.get("https://icanhazdadjoke.com/",
                            headers={"Accept": "application/json"})
    json_data = json.loads(response.content)
    joke = json_data["joke"]
    return joke

def show_list():
    with open('funny.txt') as file:
        data = file.read()

        # if empty
        if data == "":
            return("Nothing to show")
        
        list = data.split(",") if "," in data else data
        return list

def update_list(new_msg=chr):
    with open('funny.txt',"r+") as file:
        data = file.read()

        # if empty
        if data == "":
            file.write(new_msg)
            return("First entry!")

        # check if it's already in list
        list = data.split(",") if "," in data else data
        if new_msg in list:
            return "Already in the list"
        
        #update list
        else:
            file.write(","+new_msg)
            return("Updated!")




@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    msg = message.content

    if msg.startswith('$joke'):
        joke = get_joke()
        await message.channel.send(joke)

    elif any(word in msg for word in words):
        await message.channel.send(get_joke())
    
    if msg.startswith("$show"):
        list = show_list()
        await message.channel.send(list)
    
    if msg.startswith("$update "):
        update = msg.split("$update ",1)[1].strip()
        result = update_list(update)
        await message.channel.send(result)

TOKEN = os.getenv('TOKEN')
print(TOKEN)
client.run(TOKEN)
