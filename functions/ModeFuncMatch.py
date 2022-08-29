import cv2
from functions.setGUI import setGUI
from functions.common import Check_Clear, PlaySound
from functions.DesignLayout import make_4choice_layout
from functions.DesignLayout import make_fullimage_layout


# 処理の辞書割り当て ======================================================
def updateDictProc_Match(dictProc):
	dictProc_this = {
		"TEARAI_Q1"			: procMatch_Q1,
		"TEARAI_Q2"			: procMatch_Q2,
		"TEARAI_IMAGE_PROC"	: procMatch_ImageProc,
		"TEARAI_CORRECT"	: procMatch_Correct,
		"TEARAI_CLEAR"		: procMatch_Clear,
	}
	return dict(dictProc, **dictProc_this)


# レイアウト設定・辞書割り当て =============================================
def updateDictWindow_Match(dictWindow):
	layoutTearai_Q1 = make_4choice_layout("png/tea_q1.png", ["", "", "", "次へ"])
	layoutTearai_Q2 = make_4choice_layout("png/tea_q2.png", ["A", "B", "C", "D"])
	layoutTearai_Correct = make_4choice_layout("png/tea_a.png", ["", "", "", "次へ"])
	layoutTearai_Clear = make_4choice_layout("png/tea_i.png", ["", "", "", "次へ"])

	dictLayout = {
		"TEARAI_Q1"			: layoutTearai_Q1,
		"TEARAI_Q2"			: layoutTearai_Q2,
		"TEARAI_IMAGE_PROC"	: 'None',
		"TEARAI_CORRECT"	: layoutTearai_Correct,
		"TEARAI_CLEAR"		: layoutTearai_Clear,
	}
	dictWindow_this = setGUI(dictLayout)
	
	return dict(dictWindow, **dictWindow_this)

# 標準タップ座標設定 ================================================
def getDefaultAreaDefinition():
    vArea0 = [260, 520, 520, 60]
    listArea = [vArea0, ]

    return listArea

# tearai_Q1モード処理 ======================================================
def procMatch_Q1(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	proc = dictArgument["ImageProc"]

	if event == "次へ":
		proc.createWindows()
		sStartTime = cState.updateState("TEARAI_IMAGE_PROC")
		dictArgument["Start time"] = sStartTime


# tearai_ImageProcモード処理 ======================================================
def procMatch_ImageProc(dictArgument):
	cState = dictArgument["State"]
	proc = dictArgument["ImageProc"]
	cCtrlCard = dictArgument["CtrlCard"]

	isFound = proc.execute()
	cv2.waitKey(1)

	if isFound:
		cCtrlCard.write_result("tearai1", "T")

		sStartTime = cState.updateState("TEARAI_Q2")
		dictArgument["Start time"] = sStartTime

		proc.closeWindows()


# tearai_Q2モード処理 ======================================================
def procMatch_Q2(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	if event == "B":
		PlaySound("sound/correct.wav")

		cCtrlCard.write_result("tearai2", "T")

		sStartTime = cState.updateState("TEARAI_CORRECT")
		dictArgument["Start time"] = sStartTime

	elif event != "-timeout-":
		PlaySound("sound/wrong.wav")


# tearai_correctモード処理 ======================================================
def procMatch_Correct(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]

	if event == "次へ":
		sStartTime = cState.updateState("TEARAI_CLEAR")
		dictArgument["Start time"] = sStartTime


# tearai_clearモード処理 ======================================================
def procMatch_Clear(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]

	if event == "次へ":
		if Check_Clear(cCtrlCard):
			sStartTime = cState.updateState("CLEAR1")
			cCtrlCard.write_result("clear_game", "T")  # ゲームクリア済みであることを記録
		else:
			sStartTime = cState.updateState("SELECT_GAME")

		dictArgument["Start time"] = sStartTime

		# テアライをクリアしたのでプレイできないように設定
		cState.dictWindow["SELECT_GAME"]["テアライ"].update(disabled=True)

