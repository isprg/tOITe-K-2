import sys
import cv2
sys.path.append("./Classes")
from ClsImageProcessTempMatch import ClsImageProcessTempMatch

if __name__ == "__main__":
	strPlatform = 'WIN'
	sCameraNumber = 0
	sSensorWidth = 640
	sSensorHeight = 360
	sMonitorWidth = 1024
	sMonitorHeight = 600
	tplWindowName = ('full',)
	sFlipMode = 0

	proc = ClsImageProcessTempMatch(
		strPlatform, 
		sCameraNumber,
		sSensorWidth, 
		sSensorHeight, 
		sMonitorWidth, 
		sMonitorHeight,
		tplWindowName,
		sFlipMode)

	proc.createWindows()

	while True:
		isCorrect = proc.execute()
		sKey = cv2.waitKey(1) & 0xFF
		if sKey == ord('q') or isCorrect:
			del proc
			break