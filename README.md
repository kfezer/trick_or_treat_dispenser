It's a voice-powered trick or treat dispenser!! Say "trick or treat" and get candy.

![Gif of dispenser in action](e2e18ba7-75e4-43cc-80ac-684d3a8cce54.gif)

Due to Covid-19, a hands-free, socially distant method for distrubting candy was needed. Luckily, I had everything needed to whip this up.
This is a very simple voice activated treat dispenser running 2 raspberry Pis and a Matrix Voice. The key is to it running porcupine, an open source wake-word engine from PicoVoice:
https://github.com/Picovoice/Porcupine#python

It's highly optimized and light weight. So much so that this same model should be able to run on a microcontroller, theoretically, it could run on the Matrix Voice in stand-alone mode. 

Hardware Key breakdown:
2 RPis (Not really needed, but I used 2 hats)
Matrix Voice
The motor controll board from this kit: https://camjam.me/?page_id=1035, but probably any will do.

Software breakdown:
Porcupine
Matric Lite API
Paramiko 


It's all relatively easy. It's a stripped-down voice assistant and when the wakeword is handled, instead of streaming audio or processing it locally to understand intent, it just activates a motor. This is really easy to do given that this has one task: dispense candy when it hears "trick or treat"


Big thanks to the team at Matrix. Most of this code is taken from this example here:
https://github.com/matrix-io/google-assistant-matrixio-picovoice







