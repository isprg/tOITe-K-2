import cv2
import numpy as np

class ClsTemplateModel:
	def __init__(self, id:int, image:np.ndarray=None):
		'''複数画像を一つのテンプレートモデルとして扱うオブジェクト

		Parameters:
			id:インスタンスを任意識別するための値
			image:テンプレートとしてて扱う画像 (省略可)
		'''
		self.id = id
		self.temps = []
		if image is not None:
			self.addTempImage(image)

	def getId(self):
		'インスタンスの任意識別値を返す'
		return self.id

	def showTempImage(self, index:int=0, windowname:str='template'):
		'''テンプレートとして登録されている画像を表示する
		
		Parameters:
			index:リストに保存されている画像のインデックスを指定
			windowname:表示時のウィンドウの名前
		'''
		try:
			cv2.imshow(windowname, self.temps[index])
		except:
			print('対応インデックスに画像が登録されていません')

	def addTempImage(self, image:np.ndarray):
		'''テンプレート画像を追加する

		Parameters:
			image:テンプレートとして追加したい画像
		Returns:
			self.temps[-1]:登録した画像(確認用)
		'''
		self.temps.append(cv2.cvtColor(image, cv2.COLOR_BGR2GRAY))
		return self.temps[-1]

	def matches(self, img:np.ndarray):
		"""登録されたテンプレート画像をから、最も高い類似度を割り出す

		Parameters:
			img: テンプレートを探すグレースケール画像
		Returns:
			val: 複数テンプレートとの最も高い類似度の値
		"""
		val_match = -1
		for temp in self.temps:
			val, loc = self.matchFunc(img, temp)
			if val > val_match:
				val_match = val
		return val_match

	def matchFunc(self, img:np.ndarray, temp:np.ndarray):
		"""テンプレートマッチングを行い類似度と場所を返す

		Parameters:
			img: テンプレートを探すグレースケール画像
			temp: テンプレートのグレースケール画像
		Returns:
			val: 最大の類似度の値
			loc: 類似度が最大の左上の座標
		"""
		res = cv2.matchTemplate(img, temp, cv2.TM_CCOEFF_NORMED)
		min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
		return max_val, max_loc