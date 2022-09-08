import time
import pyautogui

from functions.setGUI import setGUI
from functions.common import Reset_Game, PlaySound, CheckTappedArea
from functions.DesignLayout import *


# 処理の辞書割り当て ======================================================
def updateDictProc_Speaker(dictProc):
	dictProc_this = {
		"SPEAKER_Q"			: procSpeaker_Q,
		"SPEAKER_PROCESS"	: procSpeaker_Process,
		# "SPEAKER_CORRECT" 	: procSpeaker_Correct,
		# "SPEAKER_WRONG"		: procSpeaker_Wrong,
		"SPEAKER_ANSWER"	: procSpeaker_Answer,		
		"SPEAKER_KEYWORD"	: procSpeaker_keyword,
	}
	return dict(dictProc, **dictProc_this)


# レイアウト設定・辞書割り当て =============================================
def updateDictWindow_Speaker(dictWindow):
	layoutSpeaker_Q = make_fullimage_layout("png/speaker_q.png", "SPEAKER_Q")
	layoutSpeaker_process = make_fullimage_layout("png/speaker_process.png", "SPEAKER_PROCESS")
	layoutSpeaker_Answer = make_fullimage_layout("png/speaker_answer.png", "SPEAKER_ANSWER")
	layoutSpeaker_keyword = make_fullimage_layout("png/speaker_keyword.png", "SPEAKER_KEYWORD")

	dictLayout = {
		"SPEAKER_Q"			: layoutSpeaker_Q,
		"SPEAKER_PROCESS"	: layoutSpeaker_process,
		# "SPEAKER_CORRECT"	: "None",
		# "SPEAKER_WRONG"	: "None",
		"SPEAKER_ANSWER"	: layoutSpeaker_Answer,		
		"SPEAKER_KEYWORD"	: layoutSpeaker_keyword,
    }
	dictWindow_this = setGUI(dictLayout)
	
	return dict(dictWindow, **dictWindow_this)

# 標準タップ座標設定 ================================================
def getDefaultAreaDefinition():
    vArea0 = [260, 520, 520, 60]
    listArea = [vArea0,]

    return listArea

# 問題画面タップ座標設定 ================================================
def getAreaDefinition():
    vArea0 = [260, 520, 240, 60]
    vArea1 = [535, 520, 240, 60]
    listArea = [vArea0, vArea1,]

    return listArea

# 正解座標設定 ================================================
def getCorrectAreaDefinition():
    vCorrectArea0 = [730, 260, 70, 90]
    listCorrectArea = [vCorrectArea0, ]

    return listCorrectArea

# くらわんか茶碗問題表示 ==================================================
def procSpeaker_Q(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cAudio = dictArgument["Player"]

	if event == "SPEAKER_Q":
		vPosition = pyautogui.position()
		listArea = getAreaDefinition()
		sTappedArea = CheckTappedArea(vPosition, listArea)
		print(sTappedArea)

		if sTappedArea == 0:  # 答えるをタップ
			sStartTime = cState.updateState("SPEAKER_PROCESS")
			dictArgument["Start time"] = sStartTime

		elif sTappedArea == 1:  # もういちどをタップ
			cAudio.playSound("sound/question_tahei.wav")

# 回答画面表示 ==================================================
def procSpeaker_Process(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cAudio = dictArgument["Player"]

	if event == "SPEAKER_PROCESS":
		vPosition = pyautogui.position()
		listCorrectArea = getCorrectAreaDefinition()
		sTappedArea = CheckTappedArea(vPosition, listCorrectArea)

		if sTappedArea == 0:  # 丸窓紋の茶碗をタップ
			sStartTime = cState.updateState("SPEAKER_ANSWER")
			dictArgument["Start time"] = sStartTime
			cAudio.playSound("sound/correct.wav")
		elif sTappedArea == -1: # それ以外をタップ
			cAudio.playSound("sound/wrong.wav")

# 解説表示 ================================================
def procSpeaker_Answer(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]

	if event == "SPEAKER_ANSWER":
		vPosition = pyautogui.position()
		listArea = getDefaultAreaDefinition()
		sTappedArea = CheckTappedArea(vPosition, listArea)
		print(sTappedArea)

		if sTappedArea == 0:  # 次へをタップ
			sStartTime = cState.updateState("SPEAKER_KEYWORD")
			dictArgument["Start time"] = sStartTime

# 合言葉表示 ================================================
def procSpeaker_keyword(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	if event == "SPEAKER_KEYWORD":
		vPosition = pyautogui.position()
		listArea = getDefaultAreaDefinition()
		sTappedArea = CheckTappedArea(vPosition, listArea)
		print(sTappedArea)

		if sTappedArea == 0:  # 次へをタップ
			cCtrlCard.write_result("speaker", "T")

			sStartTime = cState.updateState("SELECT_GAME")
			dictArgument["Start time"] = sStartTime

			# 指向性スピーカー問題をクリアしたのでプレイできないように設定
			cState.dictWindow["SELECT_GAME"]["くらわんか茶碗"].update(disabled=True)
