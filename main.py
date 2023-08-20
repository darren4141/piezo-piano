from machine import Pin,Timer,I2C,PWM
from time import sleep

MusicNotes = {"C4": 262,"CS4": 277,"D4": 294,
"DS4": 311,"E4": 330,"F4": 349,"FS4": 370,"G4": 392,"GS4": 415,"A4": 440,"AS4": 466,"B4": 494,"C5": 523,"CS5": 554,"D5": 587,"DS5": 622,
"E5": 659,"F5": 698,"FS5": 740,"G5": 784,"GS5": 831,"A5": 880,"AS5": 932,"B5": 988,"C6": 1047,"CS6": 1109,"D6": 1175,"DS6": 1245,"E6": 1324,
"F6": 1397,"FS6": 1480,"G6": 1568,"GS6": 1661,"A6": 1760,"AS6": 1865,"B6": 1976,"C7": 2093,"CS7": 2217,"D7": 2349,"DS7": 2489,"E7": 2637,
"F7": 2794,"FS7": 2960,"G7": 3136,"GS7": 3322,"A7": 3520,"AS7": 3729,"B7": 3951,"C8": 4186,"CS8": 4435,"D8": 4699,"DS8": 4978}

KeyToNotes = {'1' : "C4", '2' : "CS4", '3' : "D4", '4' : "DS4", '5' : "E4", '6' : "F4", '7' : "FS4", '8' : "G4", '9' : "GS4", '10' : "A4", '11' : "AS4", '12' : "B4", '13' : "C5", '14' : "CS5", '15' : "D5", '16' : "DS5"}

A = [0, 1, 2, 4, 5, 6]
B = [0, 1, 2, 3, 4, 5, 6]
C = [0, 3, 4, 5]
D = [0, 1, 2, 3, 4, 5]
E = [0, 3, 4, 5, 6]
F = [0, 4, 5, 6]
G = [0, 2, 3, 4, 5, 6]
AS = [0, 1, 2, 4, 5, 6, 7]
CS = [0, 3, 4, 5, 7]
DS = [0, 1, 2, 3, 4, 5, 7]
ES = [0, 3, 4, 5, 6, 7]
FS = [0, 4, 5, 6, 7]
GS = [0, 2, 3, 4, 5, 6, 7]

NotesToDisplay = {"C4" : C,
                  "CS4" : CS,
                  "D4" : D,
                  "DS4" : DS,
                  "E4" : E,
                  "F4" : F,
                  "FS4" : FS,
                  "G4" : G,
                  "GS4" : GS,
                  "A4" : A,
                  "AS4" : AS,
                  "B4" : B,
                  "C5" : C,
                  "CS5" : CS,
                  "D5" : D,
                  "DS5" : DS
                  }

keyName = [['1','2','3','4'],
           ['5','6','7','8'],
           ['9','10','11','12'],
           ['13','14','15','16']]
keypadRowPins = [13,12,11,10]
keypadColPins = [9,8,7,6]

row = []
col = []
keypadState = []

segments = {"a" : 0, "b" : 1, "c" : 2, "d" : 3, "e" : 4, "f" : 5, "g" : 6, "DP" : 7}
SegmentPins = [16, 17, 18, 19, 20, 21, 22, 26]

segment = []

speaker = PWM(Pin(14))

for i in keypadRowPins:
    row.append(Pin(i,Pin.IN,Pin.PULL_UP))
    keypadState.append([0,0,0,0])
    
for i in keypadColPins:
    col.append(Pin(i,Pin.OUT))
    
for v in SegmentPins:
    segment.append(Pin(v, Pin.OUT))

def off():
    for i in range(8):
        segment[i].low()
        
while True:
    for i in range(0,len(col)):
        col[i].low()
        sleep(0.005) #settling time
        for j in range(0,len(row)):
            pressed = not row[j].value()
            if(pressed and (keypadState[j][i] != pressed)): #state changed to high
                keypadState[j][i] = pressed
                #led.high()
                speaker.duty_u16(2000)
                speaker.freq(MusicNotes[KeyToNotes[keyName[j][i]]])
                for v in NotesToDisplay[KeyToNotes[keyName[j][i]]]:
                    segment[v].high()
            elif(not pressed and (keypadState[j][i] != pressed)): # state changed to low
                speaker.duty_u16(0)
                keypadState[j][i] = pressed
                off()
                #led.low()
        col[i].high()
