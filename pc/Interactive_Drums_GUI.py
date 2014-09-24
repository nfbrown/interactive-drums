from Tkinter import *
import tkFont

mode = "none"

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

songSelectionListFrame = Frame(songSelectionFrame)
songSelectionListFrame.pack(anchor = 'n', side = BOTTOM, expand = 1)
songSelectionList = Listbox(songSelectionListFrame)
songSelectionList.pack()

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
playButton = Button(playButtonFrame, text = "Play Song", font = smallFont)
playButton.pack()


##################################### End Song Selection frame and buttons ##############################


# start event loop
mainWindow.mainloop()

