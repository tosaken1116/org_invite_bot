
import discord
from discord.ext import commands
import os
import json
import requests
from dotenv import load_dotenv

intents = discord.Intents.all()

load_dotenv()

OWNER_NAME =os.getenv('OWNER_NAME')
INVITE_CHANNEL_NAME = os.getenv('INVITE_CHANNEL_NAME')
ORG_NAME=os.getenv('ORG_NAME')
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')
GITHUB_TOKEN=os.getenv('GITHUB_TOKEN')

bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot is ready. Logged in as {bot.user.name}')


@bot.event
async def on_raw_reaction_add(payload):
    channel = bot.get_channel(payload.channel_id)
    if channel.name!=INVITE_CHANNEL_NAME:
        return

    message = await channel.fetch_message(payload.message_id)
    user = message.guild.get_member(payload.user_id)
    if user.name !=OWNER_NAME:
        return
    try:
        res = parse_message(message.content)
        user_id = res["user_id"]
        invite_to_org(user_id)
        await channel.send(f"招待に成功しました <@{user.id}>")
    except Exception as e:
        await channel.send(f"招待に失敗しました <@{user.id}> cause:{str(e)}")


def parse_message(message)->object:
    split_message = message.split(":")
    if split_message[0]!="id":
        raise Exception("invalid format")
    return {"user_id":split_message[1]}


def invite_to_org(user_name):
    res =  requests.get(f"https://api.github.com/users/{user_name}")
    if res.status_code == 404:
        raise Exception("user not found")
    user_id = res.json()["id"]
    res = requests.post(f"https://api.github.com/orgs/{ORG_NAME}/invitations",data=json.dumps({
        "invitee_id":user_id,
        }),headers={
            "accept":"application/vnd.github+json",
            "Authorization":f"Bearer {GITHUB_TOKEN}",
            "X-GitHub-Api-Version": "2022-11-28"
        })
    if res.status_code == 201:
        print(f"invite {user_name} Success")
        return
    else:
        print(f"invite {user_name} Failed  {res.raw}")
        raise Exception(f"Failed to invite {res.raw}")

if __name__ == '__main__':
    bot.run(DISCORD_TOKEN)