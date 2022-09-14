import pyaudio
import os
import math
import time
import numpy as np
from scipy.io.wavfile import read 
from concurrent.futures import ThreadPoolExecutor
from alsa_error_handler import noalsaerr


class ClsAudioOut:
	def __init__(self):
		self.blSoundEnd = False
		self.blExecutorWorking = False
		self.blKeepAlive = False
		self.sCoundAlive = 0
		if os.name == 'nt':
			self.audio = pyaudio.PyAudio()
		else:
			with noalsaerr():
				self.audio = pyaudio.PyAudio()
	
	def __del__(self):
		self.finalize()

	def finalize(self):
		self.audio.terminate()

	def readWaveData(self, strFileName):
		self.sSampleRate, vSound = read(strFileName) 
		self.vSound = vSound / np.max(np.abs(vSound))
		self.sSoundLength = len(self.vSound) / self.sSampleRate
		print("Audio length:", self.sSoundLength)
	
	def playBufferedSound(self, sNumOfChannel):
		self.blSoundEnd = False
		stream = self.audio.open(
			format=pyaudio.paFloat32,
			channels=sNumOfChannel, 
			rate=self.sSampleRate,
			input=False,
			output=True)
		chunks = []
		chunks.append(self.vSound)
		chunk = np.concatenate(chunks)
		print("stream write")
		stream.write(chunk.astype(np.float32).tobytes())
		stream.close()
		self.blSoundEnd = True

	def playSound(self, strFileName, sNumOfChannel = 1):
		self.readWaveData(strFileName)
		self.playBufferedSound(sNumOfChannel)

	def getSoundEnd(self):
		return self.blSoundEnd

	def getKeepAlive(self):
		return self.blKeepAlive

	def setKeepAlive(self, blKeepAlive):
		self.blKeepAlive = blKeepAlive

	def playSoundAsync(self, strFileName, sNumOfChannel = 1):
		self.shutdownThread()
		self.blExecutorWorking = True
		self.executor = ThreadPoolExecutor(max_workers=1)
		self.executor.submit(self.playSound, strFileName, sNumOfChannel)

	def startKeepAlive(self, sWaitSecond):
		self.shutdownThread()
		sSampleRate = 22050
		sPlayTime = 1
		sFreq = 440
		sAmplitude = 0.05
		self.makeTone(sSampleRate, sPlayTime, sFreq, sAmplitude)
		self.blKeepAlive = True
		self.blExecutorWorking = True
		self.executor = ThreadPoolExecutor(max_workers=1)
		self.executor.submit(self.playKeepAliveTone, sWaitSecond)

	def shutdownThread(self):
		if self.blExecutorWorking == True:
			if self.blKeepAlive == True:
				self.blKeepAlive = False
				self.sCountAlive = 0			
			self.executor.shutdown()
			self.blExecutorWorking = False


	def makeTone(self, sSampleRate, sPlayTime, sFreq, sAmplitude):
		self.sSampleRate = sSampleRate
		vTime = np.linspace(0, sPlayTime, self.sSampleRate * sPlayTime)
		self.vSound = sAmplitude * np.sin(2 * math.pi * sFreq * vTime)

	def playTone(self, sSampleRate, sPlayTime, sFreq, sAmplitude):
		self.makeTone(sSampleRate, sPlayTime, sFreq, sAmplitude)
		self.playBufferedSound(1)

	def playKeepAliveTone(self, sWaitSecond):
		while True:
			time.sleep(0.5)
			print("in keep alive")
			self.sCoundAlive += 1
			if self.sCoundAlive >= sWaitSecond:
				self.playBufferedSound(1)
				self.sCoundAlive = 0
			if self.blKeepAlive == False:
				break



if __name__ == '__main__':
	from ClsAudioOut import ClsAudioOut
	cAudioOut = ClsAudioOut()
	#cAudioOut.readWaveData("card_set.wav")
	cAudioOut.playSoundAsync("final4.wav", 2)
	#cAudioOut.playSound("card_set.wav", 1)
	#cAudioOut.playTone(22050, 1, 440, 0.1)
	#cAudioOut.startKeepAlive(5)
	time.sleep(10)
	cAudioOut.finalize()
