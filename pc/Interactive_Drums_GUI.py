from Tkinter import *
import tkFont

mode = "none"
currentSong = None


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

def playSong():
	songSelectionFrame.pack_forget()
	songPlayingFrame.pack(fill = BOTH, expand = 1)
	songPlayingLabel['text'] = str(currentSong)

def on_select(event):
	playButton['state'] = 'active'
	selected = 1 + reduce(lambda rst, d: rst * 10 + d, event.widget.curselection())
	global currentSong
	currentSong = selected
	print selected

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

trainingFrame = Frame(mainFrame, bd = 7)
trainingFrame.pack(side = BOTTOM, fill = BOTH, expand = 1)
trainingModeButton = Button(trainingFrame, text = "Training Mode", command = trainingModeClicked, font = largeFont)
trainingModeButton.pack(fill = BOTH, expand = 1)
##################################### End Main Menu frame and buttons  ##################################



##################################### Start Song Selection frame and buttons ##############################
songSelectionFrame = Frame(mainWindow)

songList = StringVar()
songList.set('song1-artist1 song2-artist2 song3-artist3 song4-artist4 song5-artist5 song6-artist6 song7-artist7 song8-artist8 song9-artist9 song10-artist10 song11-artist11 song12-artist12')

songSelectionListFrame = Frame(songSelectionFrame, padx = 40, pady = 20)
songSelectionListFrame.pack(anchor = 'n', side = BOTTOM, expand = 1, fill = BOTH)
scrollbar = Scrollbar(songSelectionListFrame, orient = VERTICAL)
songSelectionList = Listbox(songSelectionListFrame, listvariable = songList)
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

songPlayingLabel = Label(songPlayingFrame, text = "Current Song: ", font = largeFont)
songPlayingLabel.pack()



##################################### End Song Playing frame and buttons ##############################


# start event loop
mainWindow.mainloop()

