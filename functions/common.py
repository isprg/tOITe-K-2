import csv
import os
import subprocess
from datetime import datetime


# アンケート結果をCSVファイルに保存
def getDictFlag():
	dictFlag = {
		"tutorial"		: "チュートリアル",
		"match"			: "テンプレートマッチ",
		"speaker"		: "指向性スピーカー",
		"pose"			: "ポーズ推定",
		"minappa"		: "みなっぱ",
		"voice"			: "音声認識",
		"complete"		: "クリア",
	}

	return dictFlag


# クリア時刻をCSVファイルに保存
def Record_ClearTime_to_CSV(dictArgument):
	cCtrlCard = dictArgument["CtrlCard"]
	dictSaveData = cCtrlCard.read_result()
	Card_ID = cCtrlCard.getID()

	listDatetime = [Card_ID, datetime.now()]
	with open("files/clear_datetime.csv", "a") as f:
		writer = csv.writer(f)
		writer.writerow(listDatetime)


# ゲームを初期化
def Reset_Game(dictArgument):
	sStartTime = dictArgument["State"].updateState("STANDBY")
	dictArgument["ImageProc"].reset()
	dictArgument["Event"] = None
	dictArgument["Values"] = None
	dictArgument["Frame"] = 0
	dictArgument["Start time"] = sStartTime


# ゲームをクリアしたかを判定
def CheckComplete(cCtrlCard):
	dictSaveData = cCtrlCard.read_result()

	bClear = True
	for key in ["tutorial", "match", "speaker", "pose", "minappa", "voice"]:
		if dictSaveData[key] != "T":
			bClear = False
			break

	return bClear

# ゲームをクリアしたかを判定
def CheckEnding(cCtrlCard):
    dictSaveData = cCtrlCard.read_result()

    bClear = True
    for key in ["tutorial", "match", "speaker", "pose", "minappa"]:
        if dictSaveData[key] != "T":
            bClear = False
            break

    return bClear


# カードが初期状態かを確認
def isBlank(cCtrlCard):
    dictSaveData = cCtrlCard.read_result()

    bClear = True
    for key in ["tutorial", "match", "speaker", "pose", "minappa", "voice", "complete"]:
        if dictSaveData[key] == "T":
            bClear = False
            break

    return bClear

def PlaySound(path):
	if os.name != 'nt':
		subprocess.Popen(["aplay", "--quiet", path])
	else:
		subprocess.Popen(["powershell", "-c", f"(New-Object Media.SoundPlayer '{path}').PlaySync();"])
	print('play sound')


def CheckTappedArea(vPosition, listArea):
	sTappedArea = -1
	for sAreaNumber in range(len(listArea)):
		sMinX = listArea[sAreaNumber][0]
		sMaxX = listArea[sAreaNumber][0] + listArea[sAreaNumber][2]
		sMinY = listArea[sAreaNumber][1]
		sMaxY = listArea[sAreaNumber][1] + listArea[sAreaNumber][3]

		if(vPosition.x > sMinX and vPosition.x < sMaxX 
		and vPosition.y > sMinY and vPosition.y < sMaxY):
			sTappedArea = sAreaNumber
			break

	return sTappedArea
			