import time
import cv2
from functions.common import PlaySound

from ClsImageProcess import ClsImageProcess
from ClsTemplateModel import ClsTemplateModel

class ClsImageProcessTempMatch(ClsImageProcess):
	def initProcess(self):
		# 設定値
		self.threshold = 0.7  # 判定閾値
		self.adv = 0.15  # 他の相関値との差
		self.timeout = 30.0  # 制限時間(使用していない)
		self.effecttime = 2.0  # 演出表示時間
		self.sensorsize = self.sensor.getImageSize()
		self.createOverlay("images/overlay_process.png")

		# 動作フラグ
		self.isCorrect = None
		self.isMatch = False
		self.isCoda = False
		self.tempId = None

		# 音声再生フラグ
		self.PlaySound_Flag = True

		# 判定に使う領域
		self.roi_size = (150, 150)
		self.roi_lt = (156, 41)
		self.roi_rb = (
			self.roi_lt[0] + self.roi_size[0],
			self.roi_lt[1] + self.roi_size[1],
		)

		# テンプレートの登録
		self.temps = []
		self.createTemplate(1, "images/image1.png")
		self.createTemplate(2, "images/image2.png")
		self.createTemplate(3, "images/image3.png")
		self.createTemplate(4, "images/image4.png")

		# 開始時刻の計測
		self.start = time.time()

	def reset(self):
		self.isCorrect = None
		self.isMatch = False
		self.isCoda = False
		self.tempId = None
		self.PlaySound_Flag = True
		for i in range(5):
			self.sensor.read()
		self.createOverlay("images/overlay_process.png")

	def createOverlay(self, imgPath: str):
		"""オーバーレイを変更する

		Parameters:
				imgPath:画像のパスを指定
		"""
		image = cv2.imread(imgPath, -1)
		mask = image[:, :, 3]
		mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2BGR)
		mask = mask / 255
		image = image[:, :, :3]
		self.window.setEnableOverlay(True, 0, 0)
		self.window.setOverlayImage(image, mask)

	def createTemplate(self, id: int, imgPath: str):
		"""テンプレートモデルを作成する

		Parameters:
				id:テンプレートのインスタンス任意識別値
				imgPath:画像のパスを指定
		Returns:
				temp:作成したテンプレートインスタンス(確認用)
		"""
		src = cv2.imread(imgPath)
		size = self.roi_size
		img = cv2.resize(src, dsize=size)
		temp = ClsTemplateModel(id, img)
		mags = [1.03, 0.95, 0.9, 0.85]  # 拡大率をここに入れる
		for mag in mags:
			size = (int(self.roi_size[0] * mag), int(self.roi_size[1] * mag))
			img = cv2.resize(src, dsize=size)
			temp.addTempImage(img)
		self.temps.append(temp)
		return temp

	def process(self):
		frame = self.imSensor

		# 終了までの処理
		if self.isCoda:
			if (time.time() - self.start) > self.effecttime:
				if self.isCorrect is True:
					return True
				elif self.isCorrect is False:
					self.isCorrect = None
					return False
				else:
					self.createOverlay("images/overlay_process.png")
					self.isCoda = False

				self.PlaySound_Flag = True

		# 演出処理
		elif self.isMatch:
			if self.tempId is None:
				# 時間切れ
				self.isCorrect = None
			elif self.tempId == 1:
				# 正解演出
				self.isCorrect = True
				self.createOverlay("images/overlay_correct.png")
			else:
				# 不正解
				self.isCorrect = False
				self.createOverlay("images/overlay_wrong.png")
			self.start = time.time()
			self.isMatch = False
			self.isCoda = True

			# 音声再生
			if self.PlaySound_Flag:
				if self.tempId == 1:
					PlaySound("sound/correct.wav")
				elif self.tempId is not None:
					PlaySound("sound/wrong.wav")
				self.PlaySound_Flag = False

		# 判定処理
		if not self.isCorrect:
			roi = frame[
				self.roi_lt[1] - 10 : self.roi_rb[1] - 10,
				self.roi_lt[0] + 10 : self.roi_rb[0] + 10,
			]
			roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

			# 全てのテンプレートの相関度を比較し、
			# 最も高いテンプレートを抽出
			val_1st = -1
			val_2nd = -1
			id_1st = 0
			ids = []
			vals = []
			for temp in self.temps:
				val = temp.matches(roi)
				ids.append(temp.getId())
				vals.append(val)
				if val > val_1st:
					val_2nd = val_1st
					val_1st = val
					id_1st = temp.getId()
				elif val > val_2nd:
					val_2nd = val

			# 最も相関度が高いテンプレートが閾値を超えるかを判定
			if (val_1st >= self.threshold) and (val_1st >= (val_2nd + self.adv)):
				self.tempId = id_1st
				self.isCoda = False
				self.isMatch = True

			# タイムアウト
			# now = time.time()
			# if (now - self.start) > self.timeout:
			# 	self.isMatch = True
			print('-' * 32)
			for i in range(0, 4):
				print(f"id:{ids[i]}, val:{vals[i]}")

		# frame = self.commonUI(frame)
		self.imProcessed = frame
		return None

	def commonUI(self, frame):
		cv2.rectangle(
			img=frame,
			pt1=self.roi_lt,
			pt2=self.roi_rb,
			color=(193, 117, 0),
			thickness=1,
			lineType=cv2.LINE_AA,
		)
		# frame = cv2.flip(frame, 1)
		return frame

	def execute(self):
		"""
		Returns:
				正解: True
				不正解: False
				その他: None
		"""
		return super().execute()


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