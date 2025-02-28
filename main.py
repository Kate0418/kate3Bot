import base64
import os
import pytz
from datetime import datetime, time
from discord.ext import commands, tasks
import discord
from dotenv import load_dotenv
from openai import OpenAI
from db import db

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
    result = db("""
        SELECT id, is_valid
        FROM unmutes
        WHERE user_id = %s;
    """, (member.id,))

    if result:
        is_valid = result[0]['is_valid']
        
        if not is_valid and after.channel is not None and (before.channel is None or before.channel != after.channel):
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

@bot.command()
async def mute(ctx):
    user_id = ctx.author.id
    db("""
        UPDATE unmutes 
        SET is_valid = %s 
        WHERE user_id = %s;
    """, (False, user_id))
    
    await ctx.send("自動ミュートをオンにしました")

@bot.command()
async def unmute(ctx):
    user_id = ctx.author.id
    db("""
        INSERT INTO unmutes (user_id, is_valid) 
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE is_valid = %s;
    """, (user_id, True, True))
    
    await ctx.send("自動ミュートをオフにしました")

bot.run(token)
