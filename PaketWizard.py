# bot.py
from genericpath import samefile, sameopenfile
from io import StringIO
import os
import os.path
from wakeonlan import send_magic_packet
from discord.ext import commands
from dotenv import load_dotenv
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!", case_insensitive=False)

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

@bot.command()
async def wol_files(ctx, *, arg=''):
    await ctx.send(os.listdir("./devices/"))

@bot.command()
async def wol_device(ctx, arg):
    file_path = ("./devices/" + arg)
    if os.path.isfile(file_path):
        variables = {}
        with open(file_path, 'r') as f:
            for line in f:
                name, value = line.split("=")
                variables[name] = str(value)
        mac_addr = variables["mac_addr"].strip("\n") 
        mac_validation = bool(re.match('^' + '[\:\-]'.join(['([0-9a-f]{2})']*6) + '$', mac_addr.lower()))
        if mac_validation == True:
            send_magic_packet(mac_addr)
            await ctx.send(str("Magic Packet was sent to " + arg))
        else:
            await ctx.send("No valid MAC-Address")                             
    else:
        await ctx.send("File does not exist")
   
@bot.command()
async def wol_mac(ctx, arg):
        mac_validation = bool(re.match('^' + '[\:\-]'.join(['([0-9a-f]{2})']*6) + '$', arg.lower()))
        if mac_validation == True:
            send_magic_packet(arg)
            await ctx.send(str("Magic Packet was sent to " + arg))
        else:
            await ctx.send("No valid MAC-Address")                             


bot.run(TOKEN)
