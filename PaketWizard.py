# bot.py
import os
import os.path
from wakeonlan import send_magic_packet
from discord.ext import commands
from dotenv import load_dotenv
import re

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix="!", case_insensitive=False)

regex_ip = "^((25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$"

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')


@bot.command()
async def files(ctx):
    await ctx.send(os.listdir("./devices/"))

@bot.command()
async def device(ctx, arg):
    file_path = ("./devices/" + arg)
    if os.path.isfile(file_path):
        variables = {}
        with open(file_path, 'r') as f:
            for line in f:
                name, value = line.split("=")
                variables[name] = str(value)
        mac_addr = variables["mac_addr"].strip("\n")
        ip_addr = variables["ip_addr"].strip("\n")
        port_addr = variables["port_addr"].strip("\n")
        mac_validation = bool(re.match('^' + '[\:\-]'.join(['([0-9a-f]{2})']*6) + '$', mac_addr.lower()))
        if mac_validation == True:
            if(re.search(regex_ip, ip_addr)):
                port_validation = int(port_addr) in range(0, 65536)
                if port_validation ==  True:  
                        send_magic_packet(mac_addr, ip_address=str(ip_addr), port=int(port_addr))
                        await ctx.send(str("Magic Packet was sent to " + arg))
                else:
                    await ctx.send("Invalid Port")
            else:
                await ctx.send("Invalid IP-Address")     
        else:
            await ctx.send("Invalid MAC-Address")                             
    else:
        await ctx.send("File does not exist")
   
@bot.command()
async def custom(ctx, custom_mac, custom_ip = "255.255.255.255", custom_port = "9"):
        custom_mac_validation = bool(re.match('^' + '[\:\-]'.join(['([0-9a-f]{2})']*6) + '$', custom_mac.lower()))
        if custom_mac_validation == True:
            if(re.search(regex_ip, custom_ip)):
                custom_port_validation = int(custom_port) in range(0, 65536)
                if custom_port_validation ==  True:
                    send_magic_packet(custom_mac, ip_address=str(custom_ip), port=int(custom_port))
                    await ctx.send("Magic Packet was sent to MAC-Address " + custom_mac + " , IP-Address " + custom_ip + " and Port " + custom_port)
                else: 
                    await ctx.send("Invalid Port")
            else: 
                await ctx.send("Invalid IP-Address") 
        else:
            await ctx.send("Not a valid MAC-Address")                             
bot.run(TOKEN)

