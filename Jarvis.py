import pyaudio
import wave
import audioop
import requests
import json
import sys
import time
import struct
import math
import os
#so far this needs FLAC download to run
from collections import deque

#CONSTANTS
CHUNK = 1024
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE = 44100 #sampling frequency in hertz
RECORD_SECONDS = 15
THRESHOLD = 0.040 #root mean square value where initial word is detected
SHORT_NORMALIZE = (1.0/32768.0)
INPUT_BLOCK_TIME = 0.01
INPUT_FRAMESPERBLOCK = int(RATE*INPUT_BLOCK_TIME)
QUIETTHRESHOLDTIME = 7 #number of frames silence before sending off


#read apis from file
def apiRead(wolframAPI):
        apiFile=open("AppIDs.txt","r")
        wolframAPI=apiFile.readline()
        wolframAPI=wolframAPI[wolframAPI.strip().find("=")+1:]
        apiFile.close()
        print "Wolfram API loaded: " + wolframAPI
        
#calculation of loudness in a given block
def rootMeanSquare(block):
        count = len(block)/2
        format = "%dh"%(count)
        shorts = struct.unpack(format,block)
        squaresum= 0.0
        for i in shorts:
                n = i* SHORT_NORMALIZE
                squaresum+=n*n
        return math.sqrt(squaresum/count)

#send audio to google speech
#incomplete - still needs to send file given in parameter of function
def sendSTT ():
        #pfilter = censor
        #xjerr = 1 tells server to return errors as part of JSON response and not HTTP codes
        speech_params = {'client':'chromium', 'lang':'en-US','maxresults':'5', 'pfilter':'0'}
        #rate = bitrate (change later to bitrate of flac file)
        speech_header = {'Content-Type':'audio/x-flac; rate = 16000;'}
        r = requests.get("https://www.google.com/speech-api/v1/recognize", params=speech_params)
        print r.url
        
def wav_toFlac (wavFileName):
        os.system(FLAC_CONV + ' ' + wavFileName
        
        
wolfAPI = ""
apiRead(wolfAPI)
sendSTT()


if raw_input("T/F start audio recording:")=="T":
        #INSTANTIATE PYAUDIO

        p=pyaudio.PyAudio()
        
        #stream = p.open (format = p.get_format_from_width(wf.getsampwidth()), channels = wf.getnchannels(), rate = wf.getframerate(), output = True,stream_callback=callback)
        stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = INPUT_FRAMESPERBLOCK)
        #stream.start_stream()

        print ("Recording")
        
        for i in range(60):#range 30 needs to become a while loop during final program
                print("Block " + str(i))
                #read block
                block = stream.read(INPUT_FRAMESPERBLOCK)
                #find amplitude of block
                amplitude = rootMeanSquare(block)
                #if amplitude is greater than threshold we assume someone is talking so we record until the next silence
                if amplitude > THRESHOLD:
                        print ("greater than threshold")
                        frames = []
                        stillTalking = True
                        quietTime = 0
                        while stillTalking==True:
                                
                                data = stream.read(INPUT_FRAMESPERBLOCK)
                                print("quiet" + str(quietTime))
                                frames.append(data)
                                #if block is quiet
                                if len(frames)>2:
                                        print 
                                        if (rootMeanSquare(data)<THRESHOLD) & (rootMeanSquare(frames[len(frames)-1])<THRESHOLD):
                                                #add one to quiet block counter
                                                quietTime +=1
                                #if quietTime meets a threshold then no talking so stop recording
                                if quietTime>QUIETTHRESHOLDTIME:
                                        stillTalking=False
                        
                        #take frames and export it to .wav file
                        wf = wave.open("firstword.wav", "wb")
                        wf.setnchannels(CHANNELS)
                        wf.setsampwidth(p.get_sample_size(FORMAT))
                        wf.setframerate(RATE)
                        wf.writeframes(b''.join(frames))
                        wf.close()
                        print ("output.wav written")
                

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


r=requests.get("http://api.wolframalpha.com/v2/query?input=pi&appid="+wolfAPI)
print (r.text)
