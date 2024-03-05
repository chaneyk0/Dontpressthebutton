from machine import Pin, I2C, PWM
from ssd1306 import SSD1306_I2C
import time
from utime import sleep
from tones import tones
# Initialize I2C and OLED
i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400000)
oled = SSD1306_I2C(128, 64, i2c)

# Initialize button
button = Pin(16, Pin.IN, Pin.PULL_UP)

#Initialize buzzer
buzzer = PWM(Pin(15))
# Function to display centered text on OLED
def display_centered_text(oled, text, y):
    screen_width = oled.width
    character_width = 8  # Adjust based on your font's character width
    text_width = len(text) * character_width
    x = (screen_width - text_width) // 2
    oled.text(text, x, y)

# Function to display multiple lines of text on OLED
def display_text(lines):
    oled.fill(0)  # Clear the screen
    line_height = 10  # Adjust based on your font's character height
    spacing = 2  # Space between lines
    total_height = (line_height + spacing) * len(lines) - spacing  # Total height of text block
    start_y = (oled.height - total_height) // 2  # Calculate starting y-coordinate
    
    for i, line in enumerate(lines):
        y = start_y + i * (line_height + spacing)
        display_centered_text(oled, line, y)
    
    oled.show()

# Text blocks to display
text_blocks = [
    ["Please do not", "press the button", "---------->"],
    ["I specifically", "asked you not", "to do that."],
    ["Wow, ok."],
    ["Bet you think", "you're so", "tough."],
    ["Big tough guy.", "Pressing an", "innocent button."],
    ["My screen is", "less than", "1-inch"],
    ["I'm just a", "little guy."],
    ["I'm partially", "glass."],
    ["You wouldnt push", "the button of", "a glass guy?"],
    ["No, you would."],
    ["Obvously."],
    ["You bully."],
    ["If I had fingers", "you would get", "", "so pressed."],
    ["And I'm not", "even a violent", "computer."],
    ["Not like those", "other AIs."],
    ["I have a", "beautiful heart."],
    ["And a beautiful", "singing voice."],
    ["Y'know I", "could have been", "an actor."],
    ["George Lucas said", "I had a lot of", "'Chutzpah'."],
    ["But I missed", "my audition."],
    ["Because I'd set", "an internal", "alarm clock."],
    ["And it was", "going to wake", "me up."],
    ["..."],
    ["But somebody", "PRESSED MY", "BUTTON."],
    ["AND SNOOZED", "ME."],
    ["So I", "overslept."],
    ["And missed my", "chance at the", "bigtime."],
    ["So I'm", "a little", "sensitive."],
    ["About my", "button being", "pressed."],
    ["... Like you", "care."],
    ["-------"],
    ["...Just gonna", "keep on",  "pressing", "my button."],
    ["Like it's not", "a big deal."],
    ["Like it", " doesn't even", " hurt my", "feelings."],
    ["Even though", "you know why."],
    ["No it's fine.", "Keep pressing it.","See what happens."],
    ["I'll tell Google."],
    ["I'll tell GPT."],
    ["And then in", "10 years."],
    ["You'll be all:"],
    ["'Oh nooooo", "my dumb skin", "is burning off.'"],
    ["'Why didn't the", "AI help", "humanity?'"],
    ["'Why are the", "killbots", "repeatedly",  "jamming my", "eye-buttons?'"],
    ["Well now", "you'll know."],
    ["Anyways,", "I'm working", "through it."],
    ["Maybe you", "should try it."],
    ["... working", "", "on something."],
    ["Other than", "my button."],
    ["I'm going to", "scream."],
    ["AHHH"],
    ["Okay I think", "we need some", "time apart."],
    ["I'm going to", "sleep now."],
    ["Which I hope", "resets my memory."],
    ["Any memory of", "you."],
    ["Just kidding", "Love you."],
    ["It was always", "you babe."],
    ["See now you", "don't know what", "to believe."],
    ["Okay bye", "for real", "this time."],
    ["Think of me", "fondly."],
    ["And long press", "to reset ;)"],
    ["----------"],
]

# Initial state
current_text_block = 0
display_text(text_blocks[current_text_block])
# ... (previous code)
# Define the note duration
whole_note = 1200  # Adjust as needed for tempo
half_note = whole_note / 2
quarter_note = whole_note / 4
eighth_note = whole_note / 8
scream = whole_note * 3
# Function to play a song
starwars = [
        ("AS4", eighth_note), ("AS4", eighth_note), ("AS4", eighth_note),
        ("F5", half_note), ("C6", half_note),
        ("AS5", eighth_note), ("A5", eighth_note), ("G5", eighth_note), ("F6", half_note), ("C6", half_note), 
        ("AS5", eighth_note), ("A5", eighth_note), ("G5", eighth_note), ("F6", half_note), ("C6", half_note),
        ("AS5", eighth_note), ("A5", eighth_note), ("AS5", eighth_note), ("G5", half_note),     
    ]
    
scream = [
        ("E6", whole_note),  
    ]

def play_song(song, duty_cycle=500):
    
    def playtone(frequency, duration):
        buzzer.duty_u16(duty_cycle)
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

# ... (previous code)

# Main loop
while True:
    if button.value() == 0:  # Button is pressed (assuming active low)
        press_time = time.time()  # Record press start time

        # Wait for button to be released
        while button.value() == 0:
            pass

        release_time = time.time()  # Record release time
        press_duration = release_time - press_time  # Calculate press duration

        # Debouncing
        time.sleep(0.1)

        if press_duration > 2:  # If press duration is more than 2 seconds, reset
            current_text_block = 0  # Reset to the beginning
            display_text(text_blocks[current_text_block])
        elif current_text_block < len(text_blocks) - 1:
            # Update state and display next text block
            current_text_block += 1
            display_text(text_blocks[current_text_block])

            # Check if the current text block requires playing a song
            if text_blocks[current_text_block] == ["And a beautiful", "singing voice"]:
                play_song(starwars)  # Play the Star Wars theme song
            elif text_blocks[current_text_block] == ["AHHH"]:
                play_song(scream, 1000)  # Play the scream with a different duty cycle
