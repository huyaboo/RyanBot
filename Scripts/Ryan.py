import discord
from discord.ext import commands
import os
from dotenv import load_dotenv
import random
import Options
import sys

#Imports environment variables
load_dotenv()
TOKEN = os.getenv('CLIENT_TOKEN')
HOST = os.getenv('HOST_ID')
PATH = os.getenv('PFP_PATH')
IMAGE = os.getenv('PFP_IMAGE')

#Prefixes to write out commands
client = commands.Bot(command_prefix = "R!")
client.remove_command('help')

#All the trigger words for the bot
trigger = ["I\'m", "I am", "Im", "IM", "I'M", "i\'m", "i am", "im", "iM", "i'M", "i aM", "i Am", "I Am", "I aM", "I AM", "I m", "i m", "I M", "i M"]
endings = ["Good night", "good night", "gn", "Gn", "GN"]

#Global variable to store accumulated number of jokes
numJokes = 0

#When the Bot is online
@client.event
async def on_ready():
	print(f"{client.user} is ready!")
	await client.change_presence(activity=discord.Game(name="R!help"))

#Help command
@client.command(aliases = ["about", "About", "Help", "Helps", "helps"])
async def help(ctx):
	commandList = discord.Embed(
		colour = discord.Colour.red(),
		title = "Help"
	)

	file = discord.File(PATH, filename = IMAGE)
	commandList.set_thumbnail(url = f"attachment://{IMAGE}")
	commandList.add_field(name = "Overview:", value = "Ryanbot is a simple bot that greets a user whenever the user says \"I\'m\" in any context. This bot is based off of Ryan (the Demon Destroyer).", inline = False)
	commandList.add_field(name = "R!mute", value = "Mutes me.", inline = False)
	commandList.add_field(name = "R!unmute", value = "Unmutes me.", inline = True)
	commandList.add_field(name = "R!allthetime", value = "Makes me send the greeting everytime. Requires users with manage channels permissions.", inline = False)
	commandList.add_field(name = "R!sometimes", value = "Makes me send the greeting sometimes. Requires users with manage channels permissions.", inline = True)
	commandList.add_field(name = "R!chance <Integer between 0-100>", value = "Changes probability of me greeting anyone. Requires users with manage channels permissions.", inline = False)
	commandList.add_field(name = "R!status", value = "All the selected options at the moment.", inline = False)
	commandList.add_field(name = "R!<a random word>", value = "It can't hurt to try a random command right?", inline = False)

	await ctx.send(file = file, embed = commandList)

#Status of the Bot
@client.command(aliases = ["Status", "Info", "info"])
async def status(ctx):
	statusOfServer = Options.dict[f'{ctx.guild.id}']

	status = discord.Embed(
		colour = discord.Colour.green(),
		title = "Status"
	)
	if statusOfServer.isMute == True:
		status.add_field(name = "Muted:", value = "I can't talk at all.", inline = False)
	else:
		status.add_field(name = "Unmuted:", value = "I am free to talk", inline = False)
	if statusOfServer.allTime == True:
		status.add_field(name = "Frequency of my messages:", value = "I am replying to every instance.", inline = False)
	else:
		status.add_field(name = "Frequency of my messages:", value = "I am replying based upon my chance below.", inline = False)
	status.add_field(name = "Chance: ", value = f'{statusOfServer.prob}%', inline = False)
	if numJokes == 1:
		status.add_field(name = "Number of Jokes Messaged:", value = f'I have replied to {numJokes} message since being online and {Options.totalJokes} messages cumulatively.', inline = False)
	else: 
		status.add_field(name = "Number of Jokes Messaged:", value = f'I have replied to {numJokes} messages since being online and {Options.totalJokes} messages cumulatively.', inline = False)
	if statusOfServer.serverJoke == 1:
		status.add_field(name = "Number of Jokes Messaged in this server:", value = f"I have replied to 1 message in this server.", inline = False)
	else:
		status.add_field(name = "Number of Jokes Messaged in this server:", value = f"I have replied to {statusOfServer.serverJoke} messages in this server.", inline = False)

	await ctx.send(embed = status)

#Mute all replies from the bot
@client.command()
async def mute(ctx):
	changeMute = Options.dict[f'{ctx.guild.id}']
	changeMute.isMute = True

	#Change noted and sent to server
	mute = discord.Embed(
		colour = discord.Colour.blurple(),
		description = "I'm now muted."
	)
	await ctx.send(embed = mute)

#Unmute the bot
@client.command()
async def unmute(ctx):
	changeMute = Options.dict[f'{ctx.guild.id}']
	changeMute.isMute = False

	#Change noted and sent to server
	mute = discord.Embed(
		colour = discord.Colour.blurple(),
		description = "I'm now unmuted."
	)
	
	await ctx.send(embed = mute)

#Bot will reply all the time to trigger words
@client.command()
@commands.has_permissions(manage_channels = True)
async def allthetime(ctx):
	changeTime = Options.dict[f'{ctx.guild.id}']
	changeTime.allTime = True

	#Change noted and sent to server
	freq = discord.Embed(
		colour = discord.Colour.blurple(),
		description = "I'm now greeting everytime."
	)
	
	await ctx.send(embed = freq)

#Bot will reply some of the times
@client.command()
@commands.has_permissions(manage_channels = True)
async def sometimes(ctx):
	changeTime = Options.dict[f'{ctx.guild.id}']
	changeTime.allTime = False

	#Change noted and sent to server
	freq = discord.Embed(
		colour = discord.Colour.blurple(),
		description = "I\'m now greeting based upon the current chance."
	)
	
	await ctx.send(embed = freq)

#Toggle probability of the bot responding to messages
@client.command()
@commands.has_permissions(manage_channels = True)
async def chance(ctx, *,number):

	#If what the user entered is not a number
	if number.isnumeric() == False:
		chanceSet = discord.Embed(
			colour = discord.Colour.blurple(),
			description =  f'{number} is not an integer between 0 and 100. Please try the command again.'
		)
		
		await ctx.send(embed = chanceSet)

	#If what the user entered is out of bounds
	elif int(number) > 100 or int(number) < 0:
		chanceSet = discord.Embed(
			colour = discord.Colour.blurple(),
			description =  f'{number} is not an integer between 0 and 100. Please try the command again.'
		)

		await ctx.send(embed = chanceSet)
	else:
		probChange = Options.dict[f'{ctx.guild.id}']
		probChange.prob = int(number)

		#Change noted and sent to server
		chanceSet = discord.Embed(
			colour = discord.Colour.blurple(),
			description =  f'Set probability of Ryan responding to {number}%.'
		)
		
		await ctx.send(embed = chanceSet)

#Commands if a user is mad
@client.command(aliases =["ShutUp", "Shutit","shutit", "stfu", "Fuckyou","fuckyou","FuckYou", "Shutup"])
async def shutup(ctx):
	#All possible bot replies
	reply = ["Oh I'm sorry please try again", "Sheesh you are mean :(", "Please try asking nicer.", "NooOOo", "I'm sorry, I didn't catch that","You alright there mate?", "I'm sorry to whoever birthed you.", "Ok then.", "What did you just say to me you POS? I'll have you know that I'm", "You too :)"]
	
	#Chooses random message from array and sends it
	index = random.randint(0, len(reply) - 1)
	repli = discord.Embed(
		colour = discord.Colour.blurple(),
		description = f'{reply[index]}'
	)
	await ctx.send(embed = repli)

#Commands if a user is glad
@client.command(aliases = ["Pog", "pog", "poggers", "pogchamp", "Poggers", "Pogchamp", "Cutie", "cutiepie", "Cutiepie", "BAE", "bae", "Bae"])
async def cutie(ctx):
	#All possible bot replies
	reply = ["Awwwww. Thanks you too :smiling_face_with_3_hearts:", "Awww. You're so sweet thank you :smiling_face_with_3_hearts: !", "I don't care you pos >:(", ":D", ";P", "XP", "I <3 you", "Love you too :).", "<3"]
	
	#Chooses random message from array and sends it
	index = random.randint(0, len(reply) - 1)
	repli = discord.Embed(
		colour = discord.Colour.blurple(),
		description = f'{reply[index]}'
	)
	await ctx.send(embed = repli)

#Analyzes for any variation of "I'm"
@client.event
async def on_message(message):

	#Creates new option object if a server is added
	identify = f'{message.guild.id}'
	if (identify not in Options.dict):
		newOptions = Options.Options(identify)
		Options.dict[f'{message.guild.id}'] = newOptions

	toTest = Options.dict[f'{message.guild.id}']

	#Sets active to false everytime a message is sent
	if toTest.allTime == False:
		active = False

	#This is so the bot doesn't accidentally do recursion
	if message.author == client.user:
		return
	if message.author.bot:
		return

	#Chance enabled if bot's "sometimes" is enabled
	if toTest.allTime == False:
		chance = random.randint(0, 100)
		if chance < toTest.prob:
			active = True
	else: 
		active = True

	#Stores all instances of "I'm"
	indices = []

	#Bool in the case that "I'm" is at the beginning of a message
	noIndex = False

	#If the bot was unmuted and active was true
	if active == True and toTest.isMute == False:
		#If "I'm" was at the beginning of a message
		for i in range(len(trigger)):
			trigs3 = trigger[i] + " "
			#If "I'm" was the actual message sent
			if trigger[i] == message.content:
				await message.channel.send('Hi I\'m Ryan!')
				global numJokes
				numJokes+= 1
				toTest.serverJoke += 1
				Options.totalJokes += 1
				noIndex = True
			elif trigs3 in message.content and message.content.find(trigs3) == 0:
				await message.channel.send(f'Hi{message.content.split(trigger[i],1)[1]} I\'m Ryan!')
				numJokes+= 1
				toTest.serverJoke += 1
				Options.totalJokes += 1
				noIndex = True

		#If "I'm" is not at the beginning of a message
		if noIndex == False:
			for i in range(len(trigger)):
				trigs = " " + trigger[i] + " "
				trig2 = " " + trigger[i]

				#If "I'm" is at the middle or end of a message, it gets placed in indices array
				if message.content.endswith(trig2):
					indices.append(trigger[i])
				if trigs in message.content and message.content.find(trigs) != 0:
					indices.append(trigger[i])

			if len(indices) > 0:
				#Initial variable set to first element
				first = indices[0]

				#Finds the first instance of "I'm"
				for j in range(len(indices)):
					if message.content.find(indices[j]) < message.content.find(first):
						first = indices[j]

				#Prints everything out after the first instance of "I'm"
				await message.channel.send(f'Hi{message.content.split(first,1)[1]} I\'m Ryan!')
				numJokes+= 1
				toTest.serverJoke += 1
				Options.totalJokes += 1

	#So we can use commands while the bot analyzes messages
	await client.process_commands(message)

	#If the host of the bot says goodnight, the script will automatically close itself
	if message.author.id == HOST:
		for i in range(len(endings)):
			end = endings[i] + " "
			ends = " " + endings[i] + " "

			if end in message.content and message.content.find(end) == 0:
				await message.channel.send('Since my creator is leaving, I\'m also saying goodnight!')
				sys.exit()
			elif ends in message.content:
				await message.channel.send('Since my creator is leaving, I\'m also saying goodnight!')
				sys.exit()
			elif endings[i] == message.content:
				await message.channel.send('Since my creator is leaving, I\'m also saying goodnight!')
				sys.exit()

#Run client
client.run(TOKEN)