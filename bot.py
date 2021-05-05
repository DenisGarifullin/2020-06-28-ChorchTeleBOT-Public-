


import telebot
import config
import random
import sqlite3
import requests
import time


from telebot import types
#111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111111

bot = telebot.TeleBot(config.TOKEN)
Main_User_Chat_ID = config.MAIN_USER_CHAT_ID


iteration = 1
while True:
	
	f = open('LastTimeStamp.txt', 'r')			
	Last_Time_Stamp = f.read()
	print (' IN - Last_Time_Stamp:',Last_Time_Stamp,' ITERATION: ',iteration)
	iteration += 1
	# соединение с Базой Данных 
	con = sqlite3.connect(r'C:/Users/user/AppData/Roaming/ViberPC/79222926549/viber.db')						
	cursorObj = con.cursor()
	cursorObj.execute("""SELECT Contact.ClientName , MessageInfo.Body , MessageInfo.TimeStamp , MessageInfo.MessageType , MessageInfo.PayloadPath , 
	MessageInfo.StickerID , MessageInfo.ThumbnailPath 
	FROM MessageInfo LEFT JOIN Contact ON Contact.ContactID = MessageInfo.ContactID WHERE 
	MessageInfo.ChatID = '80' AND 
	MessageInfo.MessageType IN ('1', '2', '3', '4', '9') 
	ORDER BY MessageInfo.TimeStamp DESC LIMIT '20';""")			
	rows = cursorObj.fetchall()
	mes = 0
	prop = 0
	for row in reversed(rows):
		Time_Stamp = row[2]
		Message_Type = row[3]
		Payload_Path = row[4]
		Sticker_ID = row[5]
		Thumbnail_Path = row[6]
		
		if Time_Stamp > int(Last_Time_Stamp):
			if Message_Type == 1 or Message_Type == 9: 						# Текстовое сообщение ##################################################
				mes += 1
						
				bot.send_message(Main_User_Chat_ID, f'<b>{row[0]}</b>: {row[1]}',parse_mode='html')
				print (f'Time: {row[2]}    Type: {row[3]} ОТПРАВЛЕНО Сообщение {mes}')
			elif Message_Type == 2:						 # Картинка ##################################################
				if Thumbnail_Path == 'None':
					ima = open(Payload_Path,'rb')
				else:
					ima = open(Thumbnail_Path,'rb')								
				bot.send_photo(Main_User_Chat_ID, ima, caption=f'<b>{row[0]}</b>', parse_mode='html')
				mes += 1
				print (f'Time: {row[2]}    Type: {row[3]} ОТПРАВЛЕНА Картинка {mes}')
			elif Message_Type == 3:						 # Видео ##################################################
				if Thumbnail_Path == 'None':
					vid = open(Payload_Path,'rb')
				else:
					vid = open(Thumbnail_Path,'rb')
				try:
					bot.send_video(Main_User_Chat_ID, vid, supports_streaming=True)
							
				except OSError:
					print ('<ошибка отправки видео>')
					prop += 1
				else:
					mes =+ 1
					print (f'Time: {row[2]}    Type: {row[3]} ОТПРАВЛЕНО Видео {mes}')
			elif Message_Type == 4: 						# Стикер ##################################################
				if Sticker_ID >= 400 and Sticker_ID <= 453:
					mes += 1
					print (f'Time: {row[2]}    Tipe: {row[3]} ОТПРАВЛЕН Стикер {mes}')
					way_sti = f'C:/Users/user/AppData/Roaming/ViberPC/data/stickers/60/400/00000{Sticker_ID}.png'
					sti = open(way_sti,'rb')
					bot.send_sticker(Main_User_Chat_ID, sti)
				if Sticker_ID == 4118:
					mes += 1
					print (f'Time: {row[2]}    Tipe: {row[3]} ОТПРАВЛЕН Стикер')
					way_sti = f'C:/Users/user/AppData/Roaming/ViberPC/data/stickers/60/400/00000454.png'
					sti = open(way_sti,'rb')
					bot.send_sticker(Main_User_Chat_ID, sti)
				else:
					prop += 1
					print ('<Незнакомый Стикер>')
			else:
				pass
		else:
			prop += 1
			con.close()
			#print (f'Time: {row[2]}    Type: {row[3]} ПРОПУЩЕНО')
	if mes == 0:
		pass
	else:
		pass
	print (f'OUT - Last_Time_Stamp: {Time_Stamp} ПРОПУЩЕНО: {prop} ОТПРАВЛЕНО: {mes}')
	print()
	f = open('LastTimeStamp.txt', 'w')
	f.write(str(Time_Stamp))
	f.close()
	time.sleep(10)
