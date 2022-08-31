import cv2
import pyautogui

from functions.setGUI import setGUI
from functions.common import CheckComplete, PlaySound, CheckTappedArea
from functions.DesignLayout import *


# 処理の辞書割り当て ======================================================
def updateDictProc_Match(dictProc):
	dictProc_this = {
		"MATCH_Q"		: procMatch_Q,
		"MATCH_PROCESS"	: procMatch_Process,
		# "MATCH_CORRECT" : procMatch_Correct,
		# "MATCH_WRONG"	: procMatch_Wrong,
		"MATCH_ANSWER"	: procMatch_Answer,		
		"MATCH_keyword"	: procMatch_keyword,
	}
	return dict(dictProc, **dictProc_this)


# レイアウト設定・辞書割り当て =============================================
def updateDictWindow_Match(dictWindow):
	layoutMatch_Q = make_fullimage_layout("png/match_q.png", "MATCH_Q")
	layoutMatch_Answer = make_fullimage_layout("png/match_answer.png", "MATCH_ANSWER")
	layoutMatch_keyword = make_fullimage_layout("png/match_keyword.png", "MATCH_KEYWORD")

	dictLayout = {
		"MATCH_Q"		: layoutMatch_Q,
		"MATCH_PROCESS"	: "None",
		# "MATCH_CORRECT"	: "None",
		# "MATCH_WRONG"	: "None",
		"MATCH_ANSWER"	: layoutMatch_Answer,
		"MATCH_KEYWORD"	: layoutMatch_keyword,
	}
	dictWindow_this = setGUI(dictLayout)
	
	return dict(dictWindow, **dictWindow_this)

# 標準タップ座標設定 ================================================
def getDefaultAreaDefinition():
    vArea0 = [260, 520, 520, 60]
    listArea = [vArea0, ]

    return listArea

# 鍵屋マーク問題表示 ================================================
def procMatch_Q(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]

	if event == "MATCH_Q":
		vPosition = pyautogui.position()
		listArea = getDefaultAreaDefinition()
		sTappedArea = CheckTappedArea(vPosition, listArea)
		print(sTappedArea)

		if sTappedArea == 0:  # 次へをタップ
			sStartTime = cState.updateState("MATCH_PROCESS")
			dictArgument["Start time"] = sStartTime

# テンプレートマッチ画面 ================================================
def procMatch_Process(dictArgument):
	cState = dictArgument["State"]
	proc = dictArgument["ImageProc"]
	cCtrlCard = dictArgument["CtrlCard"]

	proc.createWindows()
	isFound = proc.execute()
	cv2.waitKey(1)

	if isFound:
		# cCtrlCard.write_result("match", "T")

		sStartTime = cState.updateState("MATCH_ANSWER")
		dictArgument["Start time"] = sStartTime

		proc.Finalize()

# 正解オーバーレイ表示 ================================================
# def procMatch_Correct(dictArgument):
# 	pass

# 不正解オーバーレイ表示 ================================================
# def procMatch_Wrong(dictArgument):
# 	pass

# 解説表示 ================================================
def procMatch_Answer(dictArgument):
	print("e")
	event = dictArgument["Event"]
	cState = dictArgument["State"]

	print("f")
	if event == "MATCH_ANSWER":
		print("g")
		vPosition = pyautogui.position()
		listArea = getDefaultAreaDefinition()
		sTappedArea = CheckTappedArea(vPosition, listArea)
		print(sTappedArea)

		if sTappedArea == 0:  # 次へをタップ
			sStartTime = cState.updateState("MATCH_KEYWORD")
			dictArgument["Start time"] = sStartTime
	print("h")

# 合言葉表示 ================================================
def procMatch_keyword(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]

	if event == "MATCH_KEYWORD":
		vPosition = pyautogui.position()
		listArea = getDefaultAreaDefinition()
		sTappedArea = CheckTappedArea(vPosition, listArea)
		print(sTappedArea)

		if sTappedArea == 0:  # 次へをタップ
			sStartTime = cState.updateState("SELECT_GAME")
			dictArgument["Start time"] = sStartTime

			# テンプレートマッチをクリアしたのでプレイできないように設定
			cState.dictWindow["SELECT_GAME"]["おちゃわん１"].update(disabled=True)
