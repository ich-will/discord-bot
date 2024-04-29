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
responding = True


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

def update_list(new_msg):
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
        
        # update list
        else:
            file.write(","+new_msg)
            return("Updated!")

def del_meme(old_msg):
    with open('funny.txt',"r+") as file:
        data = file.read()

        # if empty
        if data == "":
            return("Nothing to delete")
        
        # delete item
        list = data.split(",") if "," in data else data
        list.remove(old_msg)

        #rewrite list
        file.seek(0)
        file.truncate()
        for item in list:
            if list.index(item) == (len(list)-1):
                file.write(item)
            else:
                file.write(item+",")
        return("Deleted "+ old_msg)

        


@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))

@client.event
async def on_message(message):
    global responding
    
    if message.author == client.user:
        return
    
    msg = message.content

    if responding:
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

        if msg.startswith("$delete "):
            old_msg = msg.split("$delete ",1)[1]
            result = del_meme(old_msg)
            await message.channel.send(result)

        if message.content.startswith('shut up'):
            if message.reference is not None:
                if message.reference.resolved.author.id == client.user.id:
                    await message.channel.send("okay...")
                    responding = False
    if msg.startswith("you can talk now"):
        await message.channel.send("finally")
        responding = True


TOKEN = os.getenv('TOKEN')
print(TOKEN)
client.run(TOKEN)
