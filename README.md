# Stage_Live
This is a set of python programs which would help in the display of lyrics for performances on stage.


# How to use it?
- use the file midi2.ino for the ESP setup
- Stage_Live_Desktop is the folder where you will find the new.py to make the .lrc file
- always have the name of the song as the first line of your lyric file.
- Stage_Live_Performer has the main.py which needs to run on a raspberry pi or  the system which you are connecting to your display.

## Stage Live Desktop
- Always have something other than the lyrics on the first line of the lyric text file.

\`\`\`
Random text
Lyric line 1
Lyric line 2
...
\`\`\`

- Space bar to advance to the next line of the lyrics as you play your audio file.

## Stage live Performer
- Put your generated *.lrc files in the Lyric folder.
- syntax of the files should be
` 00_name_name.lrc
01_name1_name1.lrc
  ... `

## Things to do
-  make a pygame window that works in Windows, Mac and Linux.               Done
-  make it work in windowed mode and in full screen mode.                   Done
-  make a mode selector. I need to define the modes.                        Seperated the programs to Performer and Desktop
-  test the scaling for the graphical elements visible on the screen        To be tested on the RPI 
-  Bluetooth MIDI
-  Make a script which helps in makin our won .lrc file

## links
https://github.com/akashrchandran/syrics


## Arduino CLI HELP
arduino-cli board listall esp32


## rpi packages help
 sudo pip3 install pyautogui --break-system-packages 

## notes

- improve the esp to rpi communication
- use the new.py in the Stage_Live_Desktop to make the .lrc files
- for now use program change in midi 

# 
