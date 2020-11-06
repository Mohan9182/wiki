import speech_recognition as sr
import functions as f
import pyttsx3
from random import choice
import covid_tracker as covid
from getpass import getpass
from hashlib import md5

r = sr.Recognizer()
r.pause_threshold = 1
engine = pyttsx3.init()
engine.setProperty('rate',150)
engine.setProperty('volume',1.0)

def get_key(mode):
	speech(f'Sir! PLease Enter the Cipher key to {mode} the data')
	md5_key='3599d0ea360d7651bdd96b6a2c2e2890'
	f.key = getpass('Enter cipher key:')
	while md5(md5(f.key.encode()).hexdigest().encode()).hexdigest()!=md5_key:
		speech("Sir the cipher key doesn't match please try again")
		f.key = getpass('Enter cipher key:')
	else: speech('Cipher key Accepted sir')

def response():
	speech(choice(["No Problem Sir","Alright Sir","Will do Sir","Done Sir","Their you go Sir"]))

def listen():
	with sr.Microphone() as source:
		f.clear()
		print("I'm Listening ......")
		r.adjust_for_ambient_noise(source, duration=2)
		audio = r.listen(source)
		try:
			print('Recognizing>')
			data = r.recognize_google(audio).lower()
			print(data)
		except:
			print("I don't Understand!")
			data = listen()
		return data

def speech(data):
	engine.say(data)
	engine.runAndWait()


if __name__ == "__main__":
	vedio_url=''
	while True:
		text = listen()
		words = text.split()
		if len(words)<=1: continue
		if 'open' in words:
			if 'twitter' in words: f.web(words[1:-2],'twitter')
			elif 'instagram' in words: f.web(words[1:-2],'instagram')
			elif 'covid' in text: covid.display_data(text)
			else: f.web(words[1:],'')
			response()

		elif 'login' in words:
			speech('Please wait while log in sir')
			if 'facebook' in words: f.facebook_log()
			elif 'twitter' in words: f.twitter_log()
			response()
		
		elif 'play' in words:
			if f.vedio(words[1:]): continue
			else: vedio_url = f.web(words[1:],'youtube')
			response()

		elif 'search' in words:
			f.google_search(words[2:])
			response()

		elif 'weather' in words or 'temperature' in words:
			if 'in' in words: pos =  words.index('in')+1
			elif 'at' in words: pos = words.index('at')+1
			else: pos = len(words)
			temp,desc = f.weather(" ".join(words[pos:])) 
			print("Temperature : {} C\nDescription : {}".format(temp,desc))
			speech("Current Temperature is {} degree celsius and is appears to be {} Sir!".format(temp,desc))
			continue

		elif 'message' in words:
			if 'to' in words: contact_name = "_".join(words[words.index('to')+1:])
			else:
				speech("To whom Sir")
				contact_name = listen()
			print(contact_name)
			number = f.file_search(contact_name)
			if len(number) == 0: continue
			else:
				print("Whats the message:")
				speech("Whats the message")
				f.sendwhatmsg(number[0],listen())
			speech("Message Sent")
			continue

		elif 'download' in words:
			f.download_youtube_vedio(vedio_url)
			response()
		
		elif 'contact' in words:
			with open('encrypted_details.txt','a+') as file:
				name = input("Enter Contact name:")
				no = input("Enter Phone Number without +91:")
				file.write(f.encrypt(name+" +91"+no)+"\n")
			
		elif 'news' in words:
			if 'on' in words: news_list = f.get_news(words[words.index('on')+1:])
			else: news_list = f.get_news('')
			if not news_list:
				print("Not much at this time Sir")
				speech("Not much at this time Sir")
				continue
			for news in news_list:
				print(news['title'].replace(' - ',' by '))
				speech(news['title'].replace(' - ',' by '))
			continue
						
		elif 'rest' in text or 'sleep' in text:
			speech("good buy sir")
			break

		else:
			name = '+'.join(words[1:])
			answer = f.get_speech(name)
			print(answer)
			speech(answer)
			continue
		#else:
		#	continue