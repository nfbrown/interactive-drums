from Tkinter import *
from threading import Thread
from enum import IntEnum
import glob
import tkFont
import re
import drumserial as ds
import midiparser as mp
import time
import ttk


class Control(IntEnum):
    EMPTY = 0
    CLEAR = 1
    QUEUE_LEAD = 2
    PLAY_LEAD = 3
    QUEUE_WAIT = 4
    PLAY_WAIT = 5
    SHOW_MODE = 6
    PAUSE = 7
    EMPTY_ERR = 8
    SEQ_ERR = 9

mode = "none"
currentSong = None
originalLen = 0
packets = []
paused = True
stop = True
thread = None

drums = ds.DrumSerial()

# finds all .mid files in the same directory as this file and displays
# them alphabetically
songs = glob.glob("*.mid")
songs.sort()
finalSongs = []
for i in songs:
    i = re.sub('.mid', ' ', i)
    finalSongs.append(i)


def menuClicked():
    songSelectionFrame.pack_forget()
    mainFrame.pack(fill=BOTH, expand=1)


def displaySongs():
    songSelectionFrame.pack(fill=BOTH, expand=1)


def scoreModeClicked():
    mainFrame.pack_forget()
    global mode
    mode = "score"
    sendClear()
    displaySongs()


def trainingModeClicked():
    mainFrame.pack_forget()
    global mode
    mode = "training"
    sendClear()
    displaySongs()


def freePlayModeClicked():
    mainFrame.pack_forget()
    global mode
    mode = "free"
    sendPlay()
    displaySongs()  # this needs to be changed to a free play display


def pausePlayClicked():
    global paused, thread, stop
    if stop:
        paused = False
        stop = False
        pausePlayButton['text'] = 'Pause'
        thread.start()
    else:
        paused = not paused
        pausePlayButton['text'] = ' Play  ' if paused else 'Pause'


def playSong():
    global packets, thread, currentSong
    songSelectionFrame.pack_forget()
    songPlayingFrame.pack(fill=BOTH, expand=1)
    songPlayingLabel['text'] = currentSong
    createSongThread()


def createSongThread():
    global packets, thread
    drums.flush_buffers()
    packets = mp.midi_to_packets(re.sub(' ', '.mid', currentSong))
    thread = Thread(target=songThread)


def songThread():
    global packets, drums, stop, originalLen
    packetsRemaining = len(packets)
    originalLen = len(packets)
    sendQueue()
    print 'Filling buffer'
    time.sleep(0.1)
    for i in range(14):
        drums.send(packets.pop(0))
        time.sleep(0.1)
        if handleStop():
            return

    time.sleep(2)
    sendPlay()
    print 'Start receiving'
    print 'Packets Remaining: ' + str(packetsRemaining)
    while packetsRemaining > 0:
        if drums.check_for_packet():
            received = ds.parse_packet(drums.receive())
            if received[1] == 0:
                packetsRemaining -= 1
                songProgressBar.event_generate("<<Step>>", when="tail")
                if (len(packets) > 0):
                    p = packets.pop(0)
                    drums.send(p)
                    print 'Sending packet: ' + str(ds.parse_packet(p))
            print 'Received: ' + str(received)
        if handleStop():
            return
        waitOnPause()
    print 'Song complete'
    sendClear()
    stopButton.event_generate("<<EmulateClick>>", when="tail")


def sendQueue():
    global mode, drums
    if mode == "score":
        print 'Sending QUEUE_LEAD'
        drums.send(ds.create_packet(0, int(Control.QUEUE_LEAD), 0, 0))
    elif mode == "training":
        print 'Sending QUEUE_WAIT'
        drums.send(ds.create_packet(0, int(Control.QUEUE_WAIT), 0, 0))
    elif mode == "free":
        print 'Sending SHOW_MODE'
        drums.send(ds.create_packet(0, int(Control.SHOW_MODE), 0, 0))


def sendPlay():
    global mode, drums
    if mode == "score":
        print 'Sending PLAY_LEAD'
        print ds.parse_packet(ds.create_packet(0, int(Control.PLAY_LEAD), 0, 0))
        drums.send(ds.create_packet(0, int(Control.PLAY_LEAD), 0, 0))
    elif mode == "training":
        print 'Sending PLAY_WAIT'
        drums.send(ds.create_packet(0, int(Control.PLAY_WAIT), 0, 0))
    elif mode == "free":
        print 'Sending SHOW_MODE'
        drums.send(ds.create_packet(0, int(Control.SHOW_MODE), 0, 0))


def doProgressBarStep(*args):
    global originalLen
    songProgressBar.step(99.9/originalLen)


def doProgressBarReset(*args):
    songProgressBar['value'] = 0


def waitOnPause():
    global paused
    if paused is True:
        if stop is False:
            print 'Sending PAUSE'
            drums.send(ds.create_packet(0, int(Control.PAUSE), 0, 0))
        while paused:
            if handleStop():
                return
            pass
        sendPlay()


def handleStop():
    global stop, paused, drums
    if stop is True:
        sendClear()
    return stop


def sendClear():
    print 'Sending CLEAR'
    drums.send(ds.create_packet(0, Control.CLEAR, 0, 0))


def on_select(event):
    playButton['state'] = 'active'
    selected = reduce(lambda rst, d: rst * 10 + d, event.widget.curselection())
    global currentSong
    currentSong = finalSongs[selected]


def backClicked():
    global stop
    songProgressBar.event_generate("<<Reset>>", when="tail")
    songPlayingFrame.pack_forget()
    displaySongs()
    stop = True


def emulateStopClicked(*args):
    stopClicked()


def stopClicked():
    global stop, paused, thread
    stop = True
    paused = True
    pausePlayButton['text'] = ' Play  ' if paused else 'Pause'
    if isinstance(thread, Thread):
        if thread.isAlive():
            thread.join()
    createSongThread()
    songProgressBar.event_generate("<<Reset>>", when="tail")


def onClose():
    global thread, stop
    stop = True
    if isinstance(thread, Thread):
        if thread.isAlive():
            thread.join()
    drums.close()
    mainWindow.quit()

mainWindow = Tk()
mainWindow.protocol("WM_DELETE_WINDOW", onClose)

# window title
mainWindow.title("Interactive Drums")

# window dimensions
mainWindow.minsize(800, 500)
mainWindow.geometry("1100x700")

largeFont = tkFont.Font(family="Helvetica", size=36)
smallFont = tkFont.Font(family="Helvetica", size=18)

###################### Start Main Menu frame and buttons  ######################
mainFrame = Frame(mainWindow)
mainFrame.pack(fill=BOTH, expand=1)

scoreFrame = Frame(mainFrame, bd=7)
scoreFrame.pack(side=TOP, fill=BOTH, expand=1)
scoreModeButton = Button(scoreFrame, text="Score Mode",
                         command=scoreModeClicked, font=largeFont)
scoreModeButton.pack(fill=BOTH, expand=1)

freePlayFrame = Frame(mainFrame, bd=7)
freePlayFrame.pack(side=BOTTOM, fill=BOTH, expand=1)
freePlayButton = Button(freePlayFrame, text="Free Play Mode",
                        command=freePlayModeClicked, font=largeFont)
freePlayButton.pack(fill=BOTH, expand=1)

trainingFrame = Frame(mainFrame, bd=7)
trainingFrame.pack(side=BOTTOM, fill=BOTH, expand=1)
trainingModeButton = Button(trainingFrame, text="Training Mode",
                            command=trainingModeClicked, font=largeFont)
trainingModeButton.pack(fill=BOTH, expand=1)
###################### End Main Menu frame and buttons  ########################


#################### Start Song Selection frame and buttons ####################
songSelectionFrame = Frame(mainWindow)

songList = StringVar()
songstring = "".join(finalSongs)
songList.set(songstring)


songSelectionListFrame = Frame(songSelectionFrame, padx=40, pady=20)
songSelectionListFrame.pack(anchor="n", side=BOTTOM, expand=1, fill=BOTH)
scrollbar = Scrollbar(songSelectionListFrame, orient=VERTICAL)
songSelectionList = Listbox(songSelectionListFrame,
                            listvariable=songList, font=smallFont)
scrollbar.config(command=songSelectionList.yview)
scrollbar.pack(side=RIGHT, fill=Y)
songSelectionList.pack(fill=BOTH, expand=1)
songSelectionList.bind("<ButtonRelease-1>", on_select)


menuButtonFrame = Frame(songSelectionFrame)
menuButtonFrame.pack(anchor='nw', side=LEFT, expand=1)
menuButton = Button(menuButtonFrame, text="Main Menu",
                    command=menuClicked, font=smallFont)
menuButton.pack()

songSelectionLabelFrame = Frame(songSelectionFrame)
songSelectionLabelFrame.pack(anchor='n', side=LEFT, expand=1)
songSelectionLabel = Label(songSelectionLabelFrame,
                           text="Select a Song to Play", font=largeFont)
songSelectionLabel.pack()

playButtonFrame = Frame(songSelectionFrame)
playButtonFrame.pack(anchor='ne', side=LEFT, expand=1)
playButton = Button(playButtonFrame, text="Play Song", font=smallFont,
                    state=DISABLED, command=playSong)
playButton.pack()
##################### End Song Selection frame and buttons #####################


###################### Start Song Playing fram and buttons #####################
songPlayingFrame = Frame(mainWindow)

songPlayingLabel = Label(songPlayingFrame, font=largeFont)
songPlayingLabel.pack()

backButtonFrame = Frame(songPlayingFrame)
backButtonFrame.pack(anchor='nw', side=LEFT, expand=1)
backButton = Button(backButtonFrame, text="  Back  ",
                    command=backClicked, font=smallFont)
backButton.pack()

songProgressBarFrame = Frame(songPlayingFrame)
songProgressBarFrame.pack(anchor='w', side=TOP, expand=1)
songProgressBar = ttk.Progressbar(songProgressBarFrame, orient="horizontal",
                                  length=600, mode="determinate")
songProgressBar.bind("<<Step>>", doProgressBarStep)
songProgressBar.bind("<<Reset>>", doProgressBarReset)
songProgressBar.pack()


pausePlayButtonFrame = Frame(songPlayingFrame)
pausePlayButtonFrame.pack(anchor='w', side=LEFT, expand=1)
pausePlayButton = Button(pausePlayButtonFrame, text=" Play  ",
                         font=smallFont, command=pausePlayClicked)
pausePlayButton.pack()


stopButtonFrame = Frame(songPlayingFrame)
stopButtonFrame.pack(anchor='w', side=LEFT, expand=1)
stopButton = Button(stopButtonFrame, text=" Stop  ",
                    font=smallFont, command=stopClicked)
stopButton.bind("<<EmulateClick>>", emulateStopClicked)
stopButton.pack()


###################### End Song Playing frame and buttons ######################

# start event loop
mainWindow.mainloop()
