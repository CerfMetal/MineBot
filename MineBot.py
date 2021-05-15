# MineBot
# Made by Tom Croux
# Date : Sat 15 May 2021
# License : GNU General Public License v3.0 (see LICENSE)

# Initalise imports
import os
import discord
import subprocess
import asyncio
from mcstatus import MinecraftServer
import time
from spontit import SpontitResource
import yaml

# -------------------------------------------------------------------------------------------------- #
# ----------------------------------------- Variables ---------------------------------------------- #
# -------------------------------------------------------------------------------------------------- #
# Load the configuration from the config.yaml file
config = []
with open(r'config.yaml') as file:
    # The FullLoader parameter handles the conversion from YAML
    # scalar values to Python the dictionary format
    documents = yaml.load(file, Loader=yaml.FullLoader)
    for item, doc in documents.items():
        config.append(doc)

# Server Settings
ScreenPrefix, StartMinecraftServer, StartTunnel, LocalIP, Whitelist = config[0], config[1], config[2], config[3], config[4]
# Discord Settings
DiscordToken, Prefix, ServerIP, EventChannelId = config[5], config[6].lower(), config[7], config[8]
# Additional Settings
SpontitToken, SpontitUserName, ChannelName = config[9], config[10], config[11]

# Discord setup
try :
    client = discord.Client()
except :
    print("ERROR : Discord Token error")
    exit()

# Spontit setup
try :
    resource = SpontitResource(SpontitUserName, SpontitToken)
except :
    print("Error : Failed to initalise the Spontit Ressource (check username and token)")

BotName = ""

# Help on commands
commandsAdmin = []
commands = []

if ScreenPrefix == None :
    print('Set ScreenPrefix to "minecraft"')
    ScreenPrefix = "minecraft"

if StartMinecraftServer != None :
    commandsAdmin.append("start - Start the minecraft server")
    commandsAdmin.append("stop - Stop the minecraft server")
    commandsAdmin.append("send - Send a command to the minecraft server")
    commandsAdmin.append("say - Broadcast a message to the minecraft server")

commandsAdmin.append("term - Send a command to the server")

if ServerIP != None :
    commandsAdmin.append("ip - Get the ip of the minecraft server")
    commands.append("ip - Get the ip of the minecraft server")

if LocalIP != None :
    commandsAdmin.append("list - Get online players")
    commands.append("list - Get online players")

if Whitelist :
    commandsAdmin.append("add - Whitelist a player using its ign")
    commands.append("add - Whitelist a player using its ign")

commandsAdmin.append("report - Report a bug")
commands.append("report - Report a bug")

if ChannelName != None : commandsAdmin.append("event - Create an event")



Success = "👍"
Error = "🚫"
Sent = "✅"
Gaming = "🎮"
Sad = "😔"
Nice = "🤏"

# -------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------------------------- #
# ------------------------------------------ Discord ----------------------------------------------- #
# -------------------------------------------------------------------------------------------------- #
# Runs when the program is connected to the discord server
@client.event
async def on_ready():
    print("We have logged in as {0.user}".format(client))
    Loop()
    BotInfo()

# Updates the current activity of the bot - Runs every 20 seconds 
@client.event
async def ServerPresence():
    while True :
        # If the server is running
        if ServerStatus() == True :
            onlinePlayers = OnlinePlayers()
            if onlinePlayers == None or onlinePlayers == 0 :
            	try : 
            		await client.change_presence(activity=discord.Game(name="Minecraft"))
            	except : 
            		pass
            else :
            	try :
            		await client.change_presence(activity=discord.Game(name="Minecraft (" + str(onlinePlayers) + "/50)"))
            	except :
            		pass

        # If the server is closed
        elif ServerStatus() == False :
            try : 
            	await client.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="TV | " + Prefix + " help"))
            except : 
            	pass

        await asyncio.sleep(20)

# Run on new message
@client.event
async def on_message(message) :
	# Ignore messages coming from the bot
    if message.author == client.user :
        return

    # -------------------------------------------------------- #
    # ----------------------- mn start ----------------------- #
    # -------------------------------------------------------- #
	# Start the server
    elif message.content.lower().startswith(Prefix + " start") and message.author.guild_permissions.administrator and StartMinecraftServer != None :
		# If the server is not running -> start it
    	if ServerStatus() == False:
    		await message.channel.send("Opening server...")
    		Start(message.author.name)

    		# If the server started
    		if ServerStatus() == True and IPStatus() == True:
    			await message.channel.send("The server started! It should be up and running soon") and await message.add_reaction(Success)

    		# If the server didn't start
    		else :
    			# Warn the sender
    			await message.channel.send("ERROR : can't open the server!") and await message.add_reaction(Error)

    	# If the server is already running -> pass
    	else :
    		await message.channel.send("The server is already runnning!") and await message.add_reaction(Error)

    # -------------------------------------------------------- #
    # ------------------------ mn stop ----------------------- #
    # -------------------------------------------------------- #
    # Stop the server
    elif message.content.lower().startswith(Prefix + " stop") and message.author.guild_permissions.administrator and StartMinecraftServer != None :
    	# If the server is running
    	if ServerStatus() == True:
    		await message.channel.send("Stopping the server") and await message.add_reaction(Success)
    		Stop(message.author.name)

    	# If the server isn't running -> pass
    	else:
    		# Warn the sender
    		await message.channel.send("The server is not running") and await message.add_reaction(Error)

    # -------------------------------------------------------- #
    # ------------------------ mn send ----------------------- #
    # -------------------------------------------------------- #
    # Monitor the minecraft server
    elif message.content.lower().startswith(Prefix + " send") and message.author.guild_permissions.administrator:
        # If the server is running
        if ServerStatus() == True:
            await message.channel.send("Command sent!") and await message.add_reaction(Sent)
            cmd = message.content.replace(Prefix + " send ", "")
            MinecraftServerCommand(cmd, message.author.name)

        # If the server isn't running -> pass
        else:
            # Warn the sender
            await message.channel.send("The server is not running... Start the server to send a command!") and await message.add_reaction(Error)

    # -------------------------------------------------------- #
    # ----------------------- mn term ------------------------ #
    # -------------------------------------------------------- #
    # Monitor the server
    elif message.content.lower().startswith(Prefix + " term") and message.author.guild_permissions.administrator :
        await message.channel.send("Command sent!") and await message.add_reaction(Sent)
        term_Cmd = message.content.lower().replace(Prefix + " terminal ", "")
        MinecraftTerminalCommand(term_Cmd, message.author.name)

    # -------------------------------------------------------- #
    # ------------------------ mn ip ------------------------- #
    # -------------------------------------------------------- #
    # Send the ip
    elif message.content.lower().startswith(Prefix + " ip") and ServerIP != None:
        embedVar = discord.Embed(title=BotName + "Minecraft IP", description="", color=0x2B2B2B)
        if "\\n" in ServerIP :
            ServerIPList = ServerIP.split("\\n")
            for i in range (len(ServerIPList)):
                embedVar.add_field(name=ServerIPList[i].split("- ")[0], value=ServerIPList[i].split("- ")[1], inline=False)
        else :
            embedVar.add_field(name=ServerIP.split("- ")[0], value=ServerIP.split("- ")[1], inline=False)

        await message.channel.send(embed=embedVar) and await message.add_reaction(Gaming)

    # -------------------------------------------------------- #
    # ----------------------- mn help ------------------------ #
    # -------------------------------------------------------- #
    # Help with commands
    elif message.content.lower().startswith(Prefix + " help") :
        # If the sender is admin
        if message.author.guild_permissions.administrator :
            helps = commandsAdmin
            embedVar = discord.Embed(title=BotName + " Help (Administrator)", description="", color=0x2B2B2B)

    	# If the sender isn't admin
        else :
            helps = commands
            embedVar = discord.Embed(title=BotName + " Help", description="", color=0x2B2B2B)


        # Send available commmands
        for i in range (len(helps)):
            embedVar.add_field(name=Prefix + " " + helps[i].split("- ")[0], value=helps[i].split("- ")[1], inline=True)

        await message.channel.send(embed=embedVar)

    # -------------------------------------------------------- #
    # ------------------------ mn add ------------------------ #
    # -------------------------------------------------------- #
    # Whitelist player
    elif message.content.lower().startswith(Prefix + " add") and Whitelist :
        # If the server is running
        if ServerStatus() == True:
            name = message.content.replace(Prefix + " add ", "")
            MinecraftServerCommand("whitelist add " + name, None)
            await message.channel.send(name + " is now whitelisted!") and await message.add_reaction(Sent)

        # If the server isn't running -> pass
        else:
            # Warn the sender
            await message.channel.send("The server is not running... Start the server to send a command!") and await message.add_reaction(Error)

    # -------------------------------------------------------- #
    # ------------------------ mn list ----------------------- #
    # -------------------------------------------------------- #
    # Get the current online players
    elif message.content.lower().startswith(Prefix + " list") :
        # If the server is running
        if ServerStatus() == True:
            onlinePlayers = OnlinePlayers()
            if onlinePlayers == 0 or onlinePlayers == None :
                await message.channel.send("No one is curretly online") and await message.add_reaction(Sad)
            else :
                server = MinecraftServer.lookup(LocalIP)
                query = server.query()
                await message.channel.send("There are " + str(onlinePlayers) + "/50 players online : \n" + "{0}".format(", ".join(query.players.names))) and await message.add_reaction(Gaming)
            	

        # If the server isn't running
        else:
            # Warn the sender
            await message.channel.send("The server is not running... Start the server to send a command!") and await message.add_reaction(Error)

    # -------------------------------------------------------- #
    # ------------------------ mn say ------------------------ #
    # -------------------------------------------------------- #
    # Broadcast a message
    elif message.content.lower().startswith(Prefix + " say") :
        # If the server is open
        if ServerStatus() == True :
            await message.channel.send("Message sent!") and await message.add_reaction(Sent)
            msg = message.content.lower().replace(Prefix + " say ", "")
            MinecraftServerCommand("say " + msg, None)

        else:
            # Warn the operator if the server is closed
            await message.channel.send("The server is not running... Start the server to send a command!") and await message.add_reaction(Error)

    # -------------------------------------------------------- #
    # ----------------------- mn report ---------------------- #
    # -------------------------------------------------------- #
    # Report a bug
    elif message.content.lower().startswith(Prefix + " report") :
        # Console and notification info
        msg = "BUG reported : " + message.content.lower().replace(Prefix + " report ", "")
        Notification(msg)

        await message.channel.send("Problem reported!") and await message.add_reaction(Nice)

    # -------------------------------------------------------- #
    # ------------ ---------- mn event ... -------------------- #
    # -------------------------------------------------------- #
    # Create an event 
    elif message.content.lower().startswith(Prefix + " event") :
        msg = message.content.lower().replace(Prefix + " event ", "")

        EventChannel = client.get_channel(EventChannelId)

        try :
            if "\\n" in msg :
                msg = msg.split("\\n")
            
                embedVar = discord.Embed(title=msg[1], description="", color=0x2B2B2B)
                for i in range(len(msg)-2):
                    embedVar.add_field(name=msg[i+2].split("- ")[0], value=msg[i+2].split("- ")[1], inline=False)

            await EventChannel.send(msg[0])
            eventMessage = await EventChannel.send(embed=embedVar)
            await eventMessage.add_reaction(Success) and await eventMessage.channel.send(msg[0]) and await message.add_reaction(Sent)
        
        except :
            await message.channel.send("**Error** : Your command should look something like this :\nmn event <Heading> \\n <Title> \\n <Name2> - <Value2> \\n <Name2> - <Value2>...") and await message.add_reaction(Error)

        #await message.channel.purge(limit=1) and await message.channel.send(msg[0]) and await message.channel.send(embed=embedVar)

# -------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------- #


# -------------------------------------------------------------------------------------------------- #
# ----------------------------------------- Functions ---------------------------------------------- #
# -------------------------------------------------------------------------------------------------- #
# Get information about the bot
def BotInfo():
    BotNameList = ("{0.user}".format(client)).split("#")
    BotName = BotNameList[0]

# Start loopping (activity)
def Loop(): 
    loop = asyncio.get_event_loop()
    loop.call_later(5, LoopStop)
    task = loop.create_task(ServerPresence())

    try :
        loop.run_until_complete(task)
    except :
        pass

# Stop the loop
def LoopStop():
    try :
        task.cancel()
    except :
        pass

# Check the Server's status
def ServerStatus() :
    ServerStatus = str(subprocess.check_output(["screen","-list"]))
    if ScreenPrefix + "_Minecraft" in ServerStatus :
        return True
    else :
        return False

# Check the IP's status
def IPStatus() :
    ServerStatus = str(subprocess.check_output(["screen","-list"]))
    if ScreenPrefix + "_Playit" in ServerStatus :
        return True
    elif StartTunnel == None :
        return True
    else :
        return False

def OnlinePlayers():
    # Return the number of players online
    try :
        server = MinecraftServer.lookup(LocalIP)
        status = server.status()
        try : 
            if "{0}".format(status.players.online).isdigit() :
                return int("{0}".format(status.players.online))
        except :
            return 0
    except :
        pass

# Start the server
def Start(author) :
    # Start minercaft server
    os.system("screen -S " + ScreenPrefix + "_Minecraft -d -m " + StartMinecraftServer)

    # Start tunnel
    if StartTunnel != None :
        os.system("screen -S " + ScreenPrefix + "_Playit -d -m " + StartTunnel)

    # Console and notification info
    msg = author + " started the minecraft server"
    Notification(msg)

# Stop the server
def Stop(author) :
    # Stop command
    os.system("screen -S " + ScreenPrefix + "_Minecraft -X stuff 'stop ^M'")

    if StartTunnel != None :
        # Stop tunnel
        os.system("screen -S " + ScreenPrefix + "_Playit -X stuff '^C'")

    # Console and notification info
    msg = author + " stopped the minecraft server"
    Notification(msg)

# Notify important actions
def Notification(msg):
    print(msg)
    try :
        if ChannelName == None :
            resource.push(content=msg)
        else :
            resource.push(content=msg, channel_name=ChannelName)
    except :
        pass

def MinecraftServerCommand(cmd, author):
    os.system("screen -S " + ScreenPrefix + "_Minecraft -X stuff '" + cmd + "^M'")
    if author != None :
    	msg = author + " sent a command to the minecraft server : " + cmd
    	Notification(msg)

def MinecraftTerminalCommand(term_Cmd, author):
    os.system(term_Cmd)
    msg = author + " sent a command to the  server : " + term_Cmd
    Notification(msg)

# -------------------------------------------------------------------------------------------------- #
# -------------------------------------------------------------------------------------------------- #

# Start the client
client.run(DiscordToken)
