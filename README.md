interactive-drums
=================

This project contains all of the necessary software to create an interactive drum kit that teaches one how to play drums.

There are three parts to this project:

1. Embedded code for a Cypress PSoC development board
2. Python code for converting and sending MIDI information to the PSoC
3. A GUI written in Python, using the Tkinter library, for choosing songs and modes

Building for the Cypress PSoC requires the Cypress PSoC Creator IDE.

The Python code requires a few modules:

- Tkinter
- pySerial
- mido
- enum34

To see the project in action, watch [this video](https://www.youtube.com/watch?v=5bVihZEgty4&feature=youtu.be "Interactive Drums Demo").