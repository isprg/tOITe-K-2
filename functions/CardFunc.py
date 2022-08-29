

# ゲームの状態をカードに保存されているデータから設定
def SetGame_FromCard(dictArgument):
	cCtrlCard = dictArgument["CtrlCard"]
	cState = dictArgument["State"]

	dictSaveData = cCtrlCard.read_result()
	print("Save Data:", dictSaveData)

	# 全問正解の場合
	if dictSaveData is not None and dictSaveData["complete"] == "T":
		print("game complete")

	# アイスをクリアしている場合
	elif dictSaveData["ice"] == "T":
		cState.dictWindow["SELECT_GAME"]["アイス"].update(disabled=True)

	# ピザをクリアしている場合
	elif dictSaveData["pizza"] == "T":
			cState.dictWindow["SELECT_GAME"]["ピザ"].update(disabled=True)

	# ピザをクリアしている場合
	elif dictSaveData["sea"] == "T":
			cState.dictWindow["SELECT_GAME"]["海"].update(disabled=True)

	else:
		# カードを初期化
		print("InitCard")
		cCtrlCard.initCard()
		sStartTime = cState.updateState("SELECT_GAME")
		dictArgument["Start time"] = sStartTime


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