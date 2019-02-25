import requests
import os
import json
import platform
import re
import time
import getpass
import webbrowser
import subprocess

from bs4 import BeautifulSoup

my_os = platform.system()
bot_token = str(raw_input("Your bot token: "))
if bot_token:
	url = 'https://api.telegram.org/bot'+bot_token
	print url
	text = " has been connected, now you can remotely your pc from this bot"
	send_rep = requests.get(url+"/sendMessage?chat_id=580285239&text="+getpass.getuser()+"@"+platform.node()+text)
	requests.get(url+"/sendMessage?chat_id=580285239&text=Available Command:\n/shutdown - to turn off your pc\n/restart - to restart your pc\n/youtube - to search youtube videos\n/calculator - to use calculator mode\n/brightness - to change your pc brightness")
	while True:
		try:
			history_open = open('history_id.txt', 'r').read()
		except IOError:
			os.mknod('history_id.txt')
		r = requests.get(url+"/getUpdates").json()
		try:
			update_id = str(r['result'][-1]['update_id'])
		except IndexError:
			print "Command not found!"
			exit()
		if update_id in history_open:
			pass
		else:
			json_get_command = json.dumps(r['result'][-1])
			json_command = json.loads(json_get_command)
			command = str(json_command['message']['text'])
			history_save = open('history_id.txt', 'a')
			history_save.write(update_id+'\n')
			history_save.close()
			if command == "/shutdown":
				requests.get(url+"/sendMessage?chat_id=580285239&text=Command Accepted :)\nYour computer will be shutdown immediately")
				print "[+] Shutdown command received"
				time.sleep(0.5)
				print "[+] Good Bye..."
				if my_os == "Linux":
					os.system('systemctl poweroff')
				if my_os == "Windows":
					os.system('shutdown /s')
				if my_os == "Darwin":
					os.system('shutdown -h now')
				else:
					print "Your operation system is not supported yet"
					exit()
			if command == "/restart":
				requests.get(url+"/sendMessage?chat_id=580285239&text=Command Accepted :)\nYour computer will be restart immediately")
				print "[+] Restart command received"
				time.sleep(0.01)
				print "[+] See you again..."
				if my_os == "Linux":
					print "[+] Starting Restart"
					os.system('systemctl reboot')
				if my_os == "Windows":
					os.system('shutdown /r')
				if my_os == "Darwin":
					os.system('shutdown -r now')
				else:
					print "Your operation system is not supported yet"
					exit()
			if command == "/youtube":
				requests.get(url+"/sendMessage?chat_id=580285239&text=Enter your keyword\nex: Blink 182 - I miss you")
				while True:
					get_key = requests.get(url+"/getUpdates").json()
					save_key_id = str(get_key['result'][-1]['update_id'])
					if save_key_id == update_id:
						pass
					else:
						json_get_key = json.dumps(get_key['result'][-1])
						key_command = json.loads(json_get_key)
						key = str(key_command['message']['text']).replace(' ', '+')
						source_code = requests.get('https://www.youtube.com/results?search_query='+key).text.encode('ascii', 'ignore')
						soup = BeautifulSoup(source_code, 'html.parser')
						id_id = re.search('''/watch\?v=(.*)&amp;st''', str(soup)).group(1)
						video_id = id_id.split('&')[0]
						webbrowser.open_new('https://www.youtube.com/watch?v='+video_id)
						history_save = open('history_id.txt', 'a')
						history_save.write(save_key_id+'\n')
						history_save.close()
						exit()
			if command == "/calculator":
				requests.get(url+"/sendMessage?chat_id=580285239&text=Enter your number\nex: 100 * 100")
				while True:
					get_key = requests.get(url+"/getUpdates").json()
					save_key_id = str(get_key['result'][-1]['update_id'])
					if save_key_id == update_id:
						pass
					else:
						json_get_num = json.dumps(get_key['result'][-1])
						num_command = json.loads(json_get_num)
						num_ = str(num_command['message']['text']).replace(' ', '')
						num = re.split('(\*|\/|\-|\+)', num_)
						if num[1] == '*':
							rep = int(num[0]) * int(num[2])
							requests.get(url+"/sendMessage?chat_id=580285239&text=",rep)
						if num[1] == '-':
							rep = int(num[0]) - int(num[2])
							requests.get(url+"/sendMessage?chat_id=580285239&text=",rep)
						if num[1] == '+':
							rep = int(num[0]) + int(num[2])
							requests.get(url+"/sendMessage?chat_id=580285239&text=",rep)
						if num[1] == '/':
							rep = int(num[0]) / int(num[2])
							requests.get(url+"/sendMessage?chat_id=580285239&text=",rep)
						history_save = open('history_id.txt', 'a')
						history_save.write(save_key_id+'\n')
						history_save.close()
			if command == "/brightness":
				requests.get(url+"/sendMessage?chat_id=580285239&text=Input your brightness in percent\nEx: 20%")
				while True:
					get_key = requests.get(url+"/getUpdates").json()
					save_key_id = str(get_key['result'][-1]['update_id'])
					if save_key_id == update_id:
						pass
					else:
						json_get_num = json.dumps(get_key['result'][-1])
						num_command = json.loads(json_get_num)
						percent = str(num_command['message']['text']).replace('%', '')
						percentoff = float(percent) / 100
						if my_os == "Linux":
							monitor = os.popen('xrandr | grep " connected" | cut -f1 -d " "').read()
							monitor_name = str(monitor).replace('\n', '')
							commanddku = os.system('xrandr --output {} --brightness {}'.format(monitor_name,percentoff))
							exit()
						else:
							requests.get(url+"/sendMessage?chat_id=580285239&text=Your operating system not supported yet")
						history_save = open('history_id.txt', 'a')
						history_save.write(save_key_id+'\n')
						history_save.close()
			else:
				not_uderstand = "Your command is hard to understand"
				requests.get(url+"/sendMessage?chat_id=580285239&text="+not_uderstand)
