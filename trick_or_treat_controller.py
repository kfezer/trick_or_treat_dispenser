#!/usr/bin/env python3

#https://github.com/Picovoice/Porcupine#python
#https://github.com/matrix-io/google-assistant-matrixio-picovoice
import struct
import pyaudio
import pvporcupine
from matrix_lite import led
from time import sleep
from math import pi, sin
from matrix_lite import gpio

#for remote control

import paramiko

porcupine = None
pa = None
audio_stream = None

#paramiko for ssh remote control

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect("motorpi.local", username="pi", password="pi")

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
