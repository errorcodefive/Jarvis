import pyaudio
import wave
import audioop
import requests

from collections import deque

"""READ APIS FROM FILE"""
apiFile=open("AppIDs.txt","r")
wolframAPI=apiFile.readline()
wolframAPI=wolframAPI[wolframAPI.strip().find("=")+1:]
apiFile.close()

print "Wolfram API loaded: " + wolframAPI

if raw_input("T/F start audio recording:")=="T":
	CHUNK = 1024
	FORMAT = pyaudio.paInt16
	CHANNELS =2
	RATE = 44100
	RECORD_SECONDS = 15
	p=pyaudio.PyAudio()
	stream = p.open (format = FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)

	print ("Recording")
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


r=requests.get("http://api.wolframalpha.com/v2/query?input=pi&appid="+wolframAPI)
print (r.text)
