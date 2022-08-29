import time
import PySimpleGUI as sg
import pyautogui

from functions.setGUI import setGUI
from functions.common import Reset_Game, PlaySound, CheckTappedArea
from functions.CardFunc import SetGame_FromCard
from functions.DesignLayout import *


# 処理の辞書割り当て ======================================================
def createDictProc():
	dictProc = {
		"STANDBY"			: standbyModeProc,
		"TITLE"				: titleModeProc,
		"SELECT_GAME"		: select_game_ModeProc,
		"ENDING"			: endingModeProc,
		"CARD_ERROR"		: card_error_ModeProc,
	}
	return dictProc


# レイアウト設定・辞書割り当て =============================================
def createDictWindow():
	layoutBackGround = [[sg.Text()]]
	layoutStandby = make_fullimage_layout("png/standby01.png", "STANDBY")
	layoutTitle = make_fullimage_layout("png/title.png", "TITLE")
	layoutSelect_Game = make_4choice_layout("png/select01.png", ["アイス", "ピザ", "海", "画像"])
	layoutEnding = make_fullimage_layout("png/ending.png", "ENDING")
	layoutCard_Error = make_fullimage_layout("png/card_alert.png", "CARD_ERROR")

	dictLayout = {
		"BACKGROUND"  : layoutBackGround,
		"STANDBY"     : layoutStandby,
		"TITLE"       : layoutTitle,
		"SELECT_GAME" : layoutSelect_Game,
		"ENDING"      : layoutEnding,
		"CARD_ERROR"  : layoutCard_Error,
    }
	dictWindow = setGUI(dictLayout)
	
	return dictWindow


# TITLEモード処理 ======================================================
def titleModeProc(dictArgument):
	event = dictArgument["Event"]
	
	if event == "TITLE":
		# カードのデータからゲームの状態を設定
		SetGame_FromCard(dictArgument)


# STANDBYモード処理 ======================================================
def standbyModeProc(dictArgument):
	cCtrlCard = dictArgument["CtrlCard"]
	cState = dictArgument["State"]

	setFlag = cCtrlCard.setCard()

	if setFlag:
		PlaySound("sound/card_set.wav")
		sStartTime = cState.updateState("TITLE")
		dictArgument["Start time"] = sStartTime


# SELECT_GAMEモード処理 =================================================
def select_game_ModeProc(dictArgument):
	event = dictArgument["Event"]
	cState = dictArgument["State"]
	proc = dictArgument["ImageProc"]

	cCtrlCard = dictArgument["CtrlCard"]
	dictSaveData = cCtrlCard.read_result()

	if event == "アイス":
		sStartTime = cState.updateState("ICE_Q")
		dictArgument["Start time"] = sStartTime
	elif event == "ピザ":
		sStartTime = cState.updateState("PIZZA_Q")
		dictArgument["Start time"] = sStartTime
	elif event == "海":
		sStartTime = cState.updateState("SEA_Q")
		dictArgument["Start time"] = sStartTime
	elif event == "画像":
		sStartTime = cState.updateState("QR_Q")
		proc.createWindows()
		dictArgument["Start time"] = sStartTime

# ENDINGモード処理 =========================================================
def endingModeProc(dictArgument):
	event = dictArgument["Event"]
	
	if event == "ENDING":
		dictArgument["Complete"] = 1


# card_errorモード処理 ======================================================
def card_error_ModeProc(dictArgument):
	cState = dictArgument["State"]
	cCtrlCard = dictArgument["CtrlCard"]
	proc = dictArgument["ImageProc"]

	exist = cCtrlCard.check_exist()  # カードが存在するかをチェック
	identical = cCtrlCard.check_identity()  # カードが同一かをチェック
	if exist is True and identical is True:
		ReturnState, ImageProc_Flag = dictArgument["Return state"]

		if ImageProc_Flag:
			proc.createWindows()

		sStartTime = cState.updateState(ReturnState)
		dictArgument["Return state"] = None
		dictArgument["Start time"] = sStartTime

	elif identical is False or time.time() - dictArgument["Start time"] > 20:
		Reset_Game(dictArgument)