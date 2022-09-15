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
		self.sFrameLength = 8192
		self.sNumOfChannel = 1
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

	def shutdownThread(self):
		if self.blExecutorWorking == True:
			self.executor.shutdown()
			self.blExecutorWorking = False
		
		if self.blKeepAlive == True:
			self.blKeepAlive = False
			self.sCountAlive = 0

	def readWaveData(self, strFileName):
		self.sSampleRate, vSound = read(strFileName) 
		self.vSound = vSound / np.max(np.abs(vSound))
		self.sNumOfChannel = len(self.vSound.shape)
		self.sSoundLength = self.vSound.shape[0] / self.sSampleRate
		print(self.sSampleRate)
		print("Audio length:", self.sSoundLength)

	def getSoundEnd(self):
		return self.blSoundEnd

	def openStream(self):
		self.stream = self.audio.open(
			format=pyaudio.paFloat32,
			channels=self.sNumOfChannel, 
			rate=self.sSampleRate,
			#frames_per_buffer=self.sFrameLength,
			input=False,
			output=True)
		self.sSoundLength = self.vSound.shape[0]
		self.sNumOfFrames = np.int16(self.sSoundLength / self.sFrameLength) + 1
		self.sReminder = self.sFrameLength * self.sNumOfFrames - self.sSoundLength + 1		

	def closeStream(self):
		self.stream.stop_stream()
		self.stream.close()

	def playBufferedSound(self):
		self.blSoundEnd = False

		#for sFrameNumber in range(self.sNumOfFrames):
		#	sStart = self.sFrameLength * sFrameNumber
		#	sEnd = self.sFrameLength * (sFrameNumber + 1)
#
#			if sFrameNumber != self.sNumOfFrames - 1:
#				vFrame = self.vSound[sStart:sEnd]
#			elif self.sNumOfChannel == 1:
#				vFrame = np.concatenate((self.vSound[sStart:self.sSoundLength - 1],
#										np.zeros(self.sReminder,)))
#			elif self.sNumOfChannel == 2:
#				vFrame = np.concatenate((self.vSound[sStart:self.sSoundLength - 1],
#										#np.zeros((self.sReminder,self.sNumOfChannel))))
#			self.stream.write(vFrame.astype(np.float32).tobytes())
		self.stream.write(self.vSound.astype(np.float32).tobytes())
		self.blSoundEnd = True

	def playSound(self, strFileName):
		self.readWaveData(strFileName)
		self.openStream()
		self.playBufferedSound()
		self.closeStream()

	def playSoundAsync(self, strFileName):
		self.shutdownThread()
		self.blExecutorWorking = True
		self.executor = ThreadPoolExecutor(max_workers=1)
		self.executor.submit(self.playSound, strFileName)

	def getKeepAlive(self):
		return self.blKeepAlive
		
	def setKeepAlive(self, blKeepAlive):
		self.blKeepAlive = blKeepAlive

	def makeTone(self):
		sPlayTime = 2
		sFreq = 440
		sAmplitude = 0.005
		self.sSampleRate = 24000
		vTime = np.linspace(0, sPlayTime, self.sSampleRate * sPlayTime)
		self.vSound = sAmplitude * np.sin(2 * math.pi * sFreq * vTime)

	def startKeepAlive(self, sWaitSecond):
		self.shutdownThread()
		self.sNumOfChannel = 1
		self.sSampleRate = 24000
		self.blExecutorWorking = True
		self.blKeepAlive = True
		self.makeTone()
		self.openStream()
		self.executor = ThreadPoolExecutor(max_workers=1)
		self.executor.submit(self.playKeepAliveTone, sWaitSecond)

	def playKeepAliveTone(self, sWaitSecond):
		sSleepTime = 0.5
		self.sCoundAlive = 0
		while True:
			time.sleep(sSleepTime)
			self.sCoundAlive += sSleepTime
			print(self.sCoundAlive)
			if self.sCoundAlive >= sWaitSecond:
				self.playBufferedSound()
				self.sCoundAlive = 0
			if self.blKeepAlive == False:
				break
		self.closeStream()


if __name__ == '__main__':
	from ClsAudioOut import ClsAudioOut
	cAudioOut = ClsAudioOut()
	#cAudioOut.readWaveData("card_set.wav")
	#cAudioOut.playSoundAsync("final4.wav")
	cAudioOut.playSoundAsync("card_set.wav")
	#cAudioOut.playTone(22050, 2, 440, 0.1)
	cAudioOut.startKeepAlive(5)
	time.sleep(17)
	cAudioOut.setKeepAlive(False)
	print("first timer end")
	cAudioOut.startKeepAlive(5)
	time.sleep(17)
	cAudioOut.setKeepAlive(False)
	cAudioOut.finalize()
