from machine import Pin, PWM
from utime import sleep
from tones import tones

buzzer = PWM(Pin(15))

# Define the note duration
whole_note = 1200  # Adjust as needed for tempo
half_note = whole_note / 2
quarter_note = whole_note / 4
eighth_note = whole_note / 8

# Notes for the song
song = [
    ("AS4", eighth_note), ("AS4", eighth_note), ("AS4", eighth_note),
    ("F5", half_note), ("C6", half_note),
    ("AS5", eighth_note), ("A5", eighth_note), ("G5", eighth_note), ("F6", half_note), ("C6", half_note), 
    ("AS5", eighth_note), ("A5", eighth_note), ("G5", eighth_note), ("F6", half_note), ("C6", half_note),
    ("AS5", eighth_note), ("A5", eighth_note), ("AS5", eighth_note), ("G5", half_note),     
]

def playtone(frequency, duration):
    buzzer.duty_u16(300)
    buzzer.freq(frequency)
    sleep(duration / 1000)
    bequiet()

def bequiet():
    buzzer.duty_u16(0)

def playsong(mysong):
    for note, duration in mysong:
        if note == "P":
            bequiet()
        else:
            playtone(tones[note], duration)
        sleep(0.05)  # Adjust the pause between notes as needed
    bequiet()

playsong(song)
