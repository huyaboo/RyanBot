import threading

#Control variables to set in options
class Options:
	def __init__(self, guildIdentifier):
		self.isMute = False
		self.allTime = False
		self.prob = 10
		self.serverJoke = 0
		self.guild = guildIdentifier

#Open and read existing server info into dict
file = open("For_Ryan.txt", "r")
Lines = file.readlines()

#Open and read value of all jokes being made
f = open("NumJokes.txt", "r")

dict = {}
totalJokes = int(f.read())

#Reads file, parses stuff, and places previous options in dict
for line in Lines:
	values = line.split()
	dict[f'{values[0]}'] = Options(f'{values[0]}')

	if values[1] == "True":
		dict[f'{values[0]}'].isMute = True
	else:
		dict[f'{values[0]}'].isMute = False
	if values[2] == "True":
		dict[f'{values[0]}'].allTime = True
	else:
		dict[f'{values[0]}'].allTime = False

	dict[f'{values[0]}'].prob = int(values[3])
	dict[f'{values[0]}'].serverJoke = int(values[4])

file.close()
f.close()

#Threaded function that updates the text file every 10 seconds
def writeit():
	threading.Timer(10.0, writeit).start()
	file = open("For_Ryan.txt", "w+")

	for i in dict:
		if dict[i].isMute == True:
			wM = "True"
		else:
			wM = "False"
		if dict[i].allTime == True:
			aT = "True"
		else: 
			aT = "False"
		file.write(dict[i].guild + " " + wM + " " + aT + " " + f'{dict[i].prob}' + " " + f'{dict[i].serverJoke}\n')
	file.close()

	f = open("NumJokes.txt", "w+")
	f.write(f"{totalJokes}")
	f.close()

writeit()
