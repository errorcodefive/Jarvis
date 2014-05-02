import pyaudio
import wave
import audioop
import requests
import json
import sys
import time
import struct
import math
from collections import deque

#CONSTANTS
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS =2
RATE = 44100
RECORD_SECONDS = 15
THRESHOLD = 0.010
SHORT_NORMALIZE = (1.0/32768.0)
INPUT_BLOCK_TIME = 0.05
INPUT_FRAMESPERBLOCK = int(RATE*INPUT_BLOCK_TIME)
quietThresh = 60


#READ APIS FROM FILE
def apiRead():
        apiFile=open("AppIDs.txt","r")
        wolframAPI=apiFile.readline()
        wolframAPI=wolframAPI[wolframAPI.strip().find("=")+1:]
        apiFile.close()

        print "Wolfram API loaded: " + wolframAPI

def rootMeanSquare(block):
        count = len(block)/2
        format = "%dh"%(count)
        shorts = struct.unpack(format,block)
        squaresum= 0.0
        for i in shorts:
                n = i* SHORT_NORMALIZE
                squaresum+=n*n
        return math.sqrt(squaresum/count)



'''
def speechToText(inputAudio):
        url = "www.google.com"
        path =
'''
'''
#DEFINE CALLBACK
wf = wave.open("output.wav", "rb")
def callback(audio_in, frames, times, status):
        output = wf.readframes(frames)
        return (output, pyaudio.paContinue)
'''
        
apiRead()


if raw_input("T/F start audio recording:")=="T":
        #INSTANTIATE PYAUDIO

        p=pyaudio.PyAudio()
        
        #stream = p.open (format = p.get_format_from_width(wf.getsampwidth()), channels = wf.getnchannels(), rate = wf.getframerate(), output = True,stream_callback=callback)
        stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = INPUT_FRAMESPERBLOCK)
        #stream.start_stream()

        print ("Recording")
        
        for i in range(30):#range 30 needs to become a while loop during final program
                #read block
                block = stream.read(INPUT_FRAMESPERBLOCK)
                #find amplitude of block
                amplitude = rootMeanSquare(block)
                #if amplitude is greater than threshold we assume someone is talking so we record until the next silence
                if amplitude > THRESHOLD:
                        frames = []
                        stillTalking = True
                        quiteTime = 0
                        while stillTalking==True:
                                data = stream.read(INPUT_FRAMESPERBLOCK)
                                frames.append(data)
                                #if block is quiet
                                if len(frames)>2:
                                        if rootMeanSquare(data)<THRESHOLD && rootMeanSquare(frames[len(frames)])<THRESHOLD:
                                                #add one to quiet block counter
                                                quietTime +=1
                                #if quietTime meets a threshold then no talking so stop recording
                                if quietTime>quietThresh:
                                        stillTalking==False
                        
                        
                
        '''while stream.is_active():
                time.sleep(1.0)
        stream.stop_stream()
        stream.close()
        wf.close()
        p.terminate()
        '''
        '''
        frames = []
        for i in range (0,int(RATE/CHUNK*RECORD_SECONDS)):
                data = stream.read(CHUNK)
                frames.append(data)
                
        print ("Done")

        stream.stop_stream()
        stream.close()
        p.terminate()

        wf= wave.open( "output.wav","wb")
        wf.setnchannels(CHANNELS)
        wf.setsampwidth(p.get_sample_size(FORMAT))
        wf.setframerate(RATE)
        wf.writeframes(b''.join(frames))
        wf.close()
        '''


r=requests.get("http://api.wolframalpha.com/v2/query?input=pi&appid="+wolframAPI)
print (r.text)
