#!/usr/bin/env python3

#https://github.com/Picovoice/Porcupine#python
#https://github.com/matrix-io/google-assistant-matrixio-picovoice
import struct
import pyaudio
import pvporcupine
#from matrix.pushtotalk import main
from matrix_lite import led
from time import sleep
from math import pi, sin
from matrix_lite import gpio

#for remote control

import paramiko

ledAdjust = 1.01 # MATRIX Voice
everloop = ['orange'] * led.length
frequency = 0.375
counter = 0.0
tick = len(everloop) - 1


porcupine = None
pa = None
audio_stream = None

#paramiko for ssh remote control

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("motorpi.local", username="pi", password="arm123")

#set up rainbow
everloop = ['black'] * led.length

ledAdjust = 0.0
if len(everloop) == 35:
    ledAdjust = 0.51 # MATRIX Creator
else:
    ledAdjust = 1.01 # MATRIX Voice

frequency = 0.375
counter = 0.0
tick = len(everloop) - 1

def tick_rainbow():
        # Create rainbow
    for i in range(len(everloop)):
        r = round(max(0, (sin(frequency*counter+(pi/180*240))*155+100)/10))
        g = round(max(0, (sin(frequency*counter+(pi/180*120))*155+100)/10))
        b = round(max(0, (sin(frequency*counter)*155+100)/10))

        counter += ledAdjust

        everloop[i] = {'r':r, 'g':g, 'b':b}

    # Slowly show rainbow
    if tick != 0:
        for i in reversed(range(tick)):
            everloop[i] = {}
        tick -= 1

    led.set(everloop)

    sleep(.035)


def picovoice():
    try:
        porcupine = pvporcupine.create(keyword_paths = ['trick-or-treat_raspberry-pi.ppn'])

        pa = pyaudio.PyAudio()

        audio_stream = pa.open(
                        rate=porcupine.sample_rate,
                        channels=1,
                        format=pyaudio.paInt16,
                        input=True,
                        frames_per_buffer=porcupine.frame_length)

        while True:
            print("Listening")
            led.set('orange')
            #tick_rainbow()
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)

            keyword_index = porcupine.process(pcm)
            

            if keyword_index >= 0:
                print("Hotword Detected")
                audio_stream.close()
                led.set('purple')
                print("Dispensing candy")
                ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command \
                    ("python3 ~/workspace/motorreceiver.py")
                sleep(2)
                #main()
                print("Done")
                
    except KeyboardInterrupt:
        if porcupine is not None:
            porcupine.delete()
            print("deleting porc")

        if audio_stream is not None:
            audio_stream.close()
            print("closing stream")

        if pa is not None:
            pa.terminate()
            print("terminating pa")
        
            ssh.close()      
            led.set('black')
            exit(0)
                
    finally:
        if porcupine is not None:
            porcupine.delete()
            print("deleting porc")

        if audio_stream is not None:
            audio_stream.close()
            print("closing stream")

        if pa is not None:
            pa.terminate()
            print("terminating pa")
        
        picovoice()

picovoice()
