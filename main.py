import base64
import os
import pytz
from datetime import datetime, time
from discord.ext import commands, tasks
import discord
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
token = os.getenv("BOT_TOKEN")
PREFIX = '?'

intents = discord.Intents.default()
intents.messages = True
intents.reactions = True
intents.guilds = True
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(command_prefix=PREFIX, intents=intents)

@bot.event
async def on_voice_state_update(member, before, after):
    if after.channel is not None and (before.channel is None or before.channel != after.channel):
        guild_member = member.guild.get_member(member.id)
        await guild_member.edit(mute=False, deafen=False)

@bot.command()
async def send(ctx, channel_id: int, *, message: str):
    if ctx.author.id != 1086540294394237008:
        await ctx.send("権限ないで？")
        return

    channel = bot.get_channel(channel_id)
    if channel:
        await channel.send(message)

bot.run(token)
