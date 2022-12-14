from functions.common import isBlank

# ゲームの状態をカードに保存されているデータから設定
def SetGame_FromCard(dictArgument):
	cCtrlCard = dictArgument["CtrlCard"]
	cState = dictArgument["State"]

	cState.dictWindow["SELECT_GAME"]["鍵屋マーク"].update(disabled=False)
	cState.dictWindow["SELECT_GAME"]["くらわんか茶碗"].update(disabled=False)

	dictSaveData = cCtrlCard.read_result()
	print("Save Data:", dictSaveData)

	# チュートリアル未実施
	if dictSaveData is None or dictSaveData["tutorial"] != "T":
		sStartTime = cState.updateState("GO_TUTORIAL")
		dictArgument["Start time"] = sStartTime

	# # 全問正解の場合
	# elif dictSaveData["complete"] == "T":
	# 	print("game complete")

	else:
		# テンプレートマッチをクリアしている場合
		if dictSaveData["match"] == "T":
			cState.dictWindow["SELECT_GAME"]["鍵屋マーク"].update(disabled=True)
		
		# 指向性スピーカーをクリアしている場合
		if dictSaveData["speaker"] == "T":
			cState.dictWindow["SELECT_GAME"]["くらわんか茶碗"].update(disabled=True)	

	# elif isBlank(cCtrlCard):
	# 	print("InitCard")
	# 	cCtrlCard.initCard()
		
	# else:
	# 	print("all clear this machine")
		


# カードの状態をチェック
def CheckCard(dictArgument):
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]
	proc = dictArgument["ImageProc"]

	# カードが存在するかをチェック
	result = cCtrlCard.check_exist()
	if result is False:
		print("Card Error")
		if cState.dictWindow[cState.strState] == "None":
			dictArgument["Return state"] = (cState.strState, True)
			proc.closeWindows()
		else:
			dictArgument["Return state"] = (cState.strState, False)

		sStartTime = cState.updateState("CARD_ERROR")
		dictArgument["Start time"] = sStartTime

		return "CARD_ERROR"

	return cState.strState


# ゲーム終了用のカードかどうかを判定
def AdminFlag_fromCard(cCtrlCard, card_ID_list):
	ID = cCtrlCard.getID()
	if ID in card_ID_list:
		return True, ID

	return False, None