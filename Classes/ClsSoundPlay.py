import os
import subprocess
from concurrent.futures import ThreadPoolExecutor


class ClsSoundPlay:
	def __init__(self):
		self.blSoundEnd = False
		self.blExecutorWorking = False


	def playSound(self, strFileName):
		if os.name != 'nt':
			if isinstance(strFileName, str):
				subprocess.Popen(["aplay", "--quiet", strFileName])
			elif isinstance(strFileName, list):
				subprocess.Popen(["sh", "sound/play.sh", " ".join(strFileName)])
		else:
			subprocess.Popen(
				["powershell", "-c", f"(New-Object Media.SoundPlayer '{strFileName}').PlaySync();"])


	def playSoundSync(self, strFileName):
		self.blSoundEnd = False

		if os.name != 'nt':
			if isinstance(strFileName, str):
				subprocess.run(["aplay", "--quiet", strFileName])
			elif isinstance(strFileName, list):
				subprocess.run(["sh", "sound/play.sh", " ".join(strFileName)])
		else:
			subprocess.run(
				["powershell", "-c", f"(New-Object Media.SoundPlayer '{strFileName}').PlaySync();"])

		self.blSoundEnd = True


	def getSoundEnd(self):
		return self.blSoundEnd


	def playSoundEndCheck(self, strFileName):
		self.shutdownPlayThread()
		self.blExecutorWorking = True
		self.executor = ThreadPoolExecutor(max_workers=1)
		self.executor.submit(self.playSoundSync, strFileName)


	def shutdownPlayThread(self):
		if self.blExecutorWorking == True:
			self.executor.shutdown()
			self.blExecutorWorking = False