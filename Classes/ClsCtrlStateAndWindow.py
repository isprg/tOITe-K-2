import time


class ClsCtrlStateAndWindow:
	def __init__(self, strFirstWindow, strBackGround, dictWindow):
		self.dictWindow = dictWindow
		
		for sKey in self.dictWindow:
			print("init :", sKey)
			if self.dictWindow[sKey] != "None":
				window = self.dictWindow[sKey]
				window.hide()
				#window.Maximize()
				
		# 背景ウィンドウ
		window = self.dictWindow[strBackGround]
		window.un_hide()

		# 初期ウィンドウ
		window = self.dictWindow[strFirstWindow]
		window.un_hide()

		self.strState = strFirstWindow

	def Finalize(self):
		self.closeAllWindows()

	def updateState(self, strNextState):
		self.switchWindow(strNextState)
		self.strState = strNextState
		print("The current state is: ", strNextState)
		return time.time()

	def readEvent(self, timeout=500):
		window = self.dictWindow[self.strState]
		return window.read(timeout=timeout, timeout_key="-timeout-")

	def switchWindow(self, strNewState):
		if self.dictWindow[strNewState] != "None":
			self.dictWindow[strNewState].un_hide()
		if self.dictWindow[self.strState] != "None":
			self.dictWindow[self.strState].hide()

	def getState(self):
		return self.strState

	def closeAllWindows(self):
		for sKey in self.dictWindow:
			window = self.dictWindow[sKey]

			if window != "None":
				window.close()
