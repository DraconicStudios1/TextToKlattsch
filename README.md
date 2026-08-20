# TextToKlattsch
Python Webserver Package for generating audio using the Klattsch Vocal Synth by tgies

## DISCLAIMER
I DO NOT OWN THE KLATTSCH VOCAL SYNTH, ALL CREDITS GO TO tgies FOR DEVELOPING THE KLATTSCH VOCAL SYNTH.
AGAIN, I DO NOT OWN ANY OF THE CODE FOR THE KLATTSCH VOCAL SYNTH.

This is a fairly user-friendly web-package interface for the Klattsch Vocal Synth, although there already exists a website for it, that website uses a Pheonetic alphabet called Arpabet, which is a nightmare to type out manually.
So I made this, a website which allows the average user to type raw text and audio clip settings (using the Klattsch syntax), and get an audio clip out of it!
All of the configuration codes are displayed on the website's frontend (i am not a frontend developer, so the HTML frontend is written in HTML1 for my convenience.)
Have fun!

# STARTUP HELP
## WINDOWS
Step 1: Open up your CLI app of your choice (only tested with Command Prompt and Powershell 7)

### Command Prompt
Step 2A: If you have the website stored on any drive besides the one running your OS, run "cd /d {drive:/path/to/website}"
NOTE: IF IT IS ON YOUR C:/ DRIVE YOU DO NOT NEED TO PUT "/d"

Step 3A: run app.py by typing "app.py"

### Powershell 7
Step 2B: Run "cd {drive:/path/to/website}" (/d is not needed in powershell)

Step 3B: run app.py by typing "app.py"

## LINUX
NOT YET TESTED, but it should work if you tinker with it for a bit. run with sudo.
