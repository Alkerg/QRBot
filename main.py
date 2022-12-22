import discord
from PIL import Image
import qrcode
import datetime
import io
import asyncio
#import cv2
import urllib.request
import numpy as np
import os
from discord.ui import Button, View
from discord.ext import commands
from discord import app_commands
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='-', description='I can generate and read QR codes', intents=intents)

#EVENTS
@bot.event
async def on_ready():
    print("testbot is ready!")
    try:
        synced = await bot.tree.sync()
        print(f"Synced {len(synced)} commands")
    except Exception as error:
        print(error)

#COMMANDS
@bot.hybrid_command(name="ping", with_app_command=True, description="Send a ping")
async def ping(ctx):
    embed = discord.Embed(title = "¡Pong! :ping_pong:", timestamp = datetime.datetime.now(),color = discord.Color.green())
    await ctx.send(embed = embed)

@bot.hybrid_command(name="generateqr", with_app_command=True, description="Generate a QR code")
@app_commands.describe(message = "What's the message?")
async def generateqr(ctx:commands.Context, message: str):
    qr = qrcode.make(message)
    print(message)
    with io.BytesIO() as image_binary:
        qr.save(image_binary,"PNG")
        image_binary.seek(0)
        print("QR created")
        embed = discord.Embed(title="QR",timestamp=datetime.datetime.now(),color=discord.Color.blurple())
        image = discord.File(fp=image_binary,filename="qr.png")
        embed.set_image(url="attachment://qr.png")

        await ctx.send(embed=embed,file=image,ephemeral=True)
"""
#EVENTS
@bot.event
async def on_message(message):

    if message.attachments and message.author.id != 1050920821645905960:
        val,link = await scan_qr(message)
        await message.channel.send(content=val)
        
    await bot.process_commands(message)

#FUNCTIONS
async def scan_qr(message):
    detector = cv2.QRCodeDetector()
    requestSite = urllib.request.Request(str(message.attachments[0].url), headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(requestSite) as img:
        image = np.asarray(bytearray(img.read()), dtype="uint8")
        val,points,straight_qrcode = detector.detectAndDecode(cv2.imdecode(image,cv2.IMREAD_COLOR))
        link = message.attachments[0].url
        return val, link
"""
#ERRORS
@generateqr.error
async def generateqr_error(ctx,error):
    if isinstance(error, discord.ext.commands.errors.MissingRequiredArgument):
        print("No hay argumentos")

if __name__ == "__main__":
    bot.run(os.getenv('DISCORD_TOKEN'))