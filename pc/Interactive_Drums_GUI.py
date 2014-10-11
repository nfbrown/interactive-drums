from Tkinter import *
import glob
import tkFont
import re

mode = "none"
currentSong = None

# finds all .mid files in the same directory as this file and displays them alphabetically
songs = glob.glob("*.mid")
songs.sort()
finalSongs = []
for i in songs:
    i = re.sub('.mid', ' ', i)
    finalSongs.append(i)



def menuClicked():
	songSelectionFrame.pack_forget()
	mainFrame.pack(fill = BOTH, expand = 1)

def displaySongs():
	songSelectionFrame.pack(fill = BOTH, expand = 1)

def scoreModeClicked():
	mainFrame.pack_forget()
	mode = "score"
	displaySongs()
	
def trainingModeClicked():
	mainFrame.pack_forget()
	mode = "training"
	displaySongs()

def freePlayModeClicked():
	mainFrame.pack_forget()
	mode = "free"
	displaySongs()

def playSong():
	songSelectionFrame.pack_forget()
	songPlayingFrame.pack(fill = BOTH, expand = 1)
	songPlayingLabel['text'] = str(currentSong)

def on_select(event):
	playButton['state'] = 'active'
	selected = reduce(lambda rst, d: rst * 10 + d, event.widget.curselection())
	global currentSong
	currentSong = finalSongs[selected]

def backClicked():
    songPlayingFrame.pack_forget()
    displaySongs()


mainWindow = Tk()

# window title
mainWindow.title("Interactive Drums")

# window dimensions
mainWindow.minsize(800,500)
mainWindow.geometry("1100x700")

largeFont = tkFont.Font(family = "Helvetica", size = 36)
smallFont = tkFont.Font(family = "Helvetica", size = 18)

##################################### Start Main Menu frame and buttons  ##################################
mainFrame = Frame(mainWindow)
mainFrame.pack(fill = BOTH, expand = 1)


scoreFrame = Frame(mainFrame, bd = 7)
scoreFrame.pack(side = TOP, fill = BOTH, expand = 1)
scoreModeButton = Button(scoreFrame, text = "Score Mode", command = scoreModeClicked, font = largeFont)
scoreModeButton.pack(fill = BOTH, expand = 1)

freePlayFrame = Frame(mainFrame, bd = 7)
freePlayFrame.pack(side = BOTTOM, fill = BOTH, expand = 1)
freePlayButton = Button(freePlayFrame, text = "Free Play Mode", command = freePlayModeClicked, font = largeFont)
freePlayButton.pack(fill = BOTH, expand = 1)

trainingFrame = Frame(mainFrame, bd = 7)
trainingFrame.pack(side = BOTTOM, fill = BOTH, expand = 1)
trainingModeButton = Button(trainingFrame, text = "Training Mode", command = trainingModeClicked, font = largeFont)
trainingModeButton.pack(fill = BOTH, expand = 1)


##################################### End Main Menu frame and buttons  ##################################



##################################### Start Song Selection frame and buttons ##############################
songSelectionFrame = Frame(mainWindow)

songList = StringVar()
songstring = "".join(finalSongs)
songList.set(songstring)


songSelectionListFrame = Frame(songSelectionFrame, padx = 40, pady = 20)
songSelectionListFrame.pack(anchor = "n", side = BOTTOM, expand = 1, fill = BOTH)
scrollbar = Scrollbar(songSelectionListFrame, orient = VERTICAL)
songSelectionList = Listbox(songSelectionListFrame, listvariable = songList, font = smallFont)
scrollbar.config(command = songSelectionList.yview)
scrollbar.pack(side = RIGHT, fill = Y)
songSelectionList.pack(fill = BOTH, expand = 1)
songSelectionList.bind("<ButtonRelease-1>", on_select)


menuButtonFrame = Frame(songSelectionFrame)
menuButtonFrame.pack(anchor = 'nw', side = LEFT, expand = 1)
menuButton = Button(menuButtonFrame, text = "Main Menu", command = menuClicked, font = smallFont)
menuButton.pack()

songSelectionLabelFrame = Frame(songSelectionFrame)
songSelectionLabelFrame.pack(anchor = 'n', side = LEFT, expand = 1)
songSelectionLabel = Label(songSelectionLabelFrame, text = "Select a Song to Play", font = largeFont)
songSelectionLabel.pack()

playButtonFrame = Frame(songSelectionFrame)
playButtonFrame.pack(anchor = 'ne', side = LEFT, expand = 1)
playButton = Button(playButtonFrame, text = "Play Song", font = smallFont, state = DISABLED, command = playSong)
playButton.pack()


##################################### End Song Selection frame and buttons ##############################


##################################### Start Song Playing fram and buttons ###############################
songPlayingFrame = Frame(mainWindow)

songPlayingLabel = Label(songPlayingFrame, font = largeFont)
songPlayingLabel.pack()

backButtonFrame = Frame(songPlayingFrame)
backButtonFrame.pack(anchor = 'nw', side = LEFT, expand = 1)
backButton = Button(backButtonFrame, text = "Back", command = backClicked, font = smallFont)
backButton.pack()



##################################### End Song Playing frame and buttons ##############################


# start event loop
mainWindow.mainloop()

