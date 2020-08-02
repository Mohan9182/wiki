import speech_recognition as sr
import wikipedia
import time
import functions as f
import pyttsx3
import random
from multiprocessing import Process,Pipe
import covid_tracker as covid
from getpass import getpass
from hashlib import md5

r = sr.Recognizer()
r.pause_threshold = 1
engine = pyttsx3.init()
engine.setProperty('rate',150)
engine.setProperty('volume',1.0)

def get_key():
	speech('Sir! PLease Enter the Cipher key to Decrypte the data')
	md5_key='3599d0ea360d7651bdd96b6a2c2e2890'
	f.key = getpass('Enter cipher key:')
	while md5(md5(f.key.encode()).hexdigest().encode()).hexdigest()!=md5_key:
		speech("Sir! the cipher key doesn't match please try again")
		f.key = getpass('Enter cipher key:')
	else: speech('Cipher key Accepted sir')

def response():
	speech(random.choice(["No Problem Sir","Alright Sir","Will do Sir","Done Sir","Their you go Sir"]))

def listen():
	with sr.Microphone(device_index=1) as source:
		f.clear()
		print("I'm Listening ......")
		r.adjust_for_ambient_noise(source, duration=1)
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
	while True:
		text = listen()
		if 'wiki' in text or 'vicky' in text:
			words = text.split()
			if 'open' in words:
				word = words[1]
				if 'text' in words: f.application('text')
				elif 'twitter' in words: f.web(words[2:-2],'twitter')
				elif 'instagram' in words: f.web(words[2:-2],'instagram')
				#else:
				#	f.site(''.join(words[2:]))
				else: f.web(words[words.index(word)+1:],'')
			elif 'login' in words:
				speech('Please wait while log in sir')
				if 'facebook' in words: f.facebook_log()
				elif 'twitter' in words: f.twitter_log()
			elif 'play' in words:
				if f.vedio(words[2:]): continue
				else: vedio_url = f.web(words[2:],'youtube')

			#elif 'what' in words:
			#	name = ' '.join(words[3:])
			#	print(wikipedia.summary(name,sentences=3).encode("utf-8"))
			#	time.sleep(20)

			elif 'search' in words: f.google_search(words[3:])

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
				number = f.file_search(contact_name)[0]
				print("Whats the message:")
				speech("Whats the message")
				if number == 0: continue
				else: f.sendwhatmsg(number,listen())
				speech("Message Sent")
				continue

			elif 'download' in words: f.download_youtube_vedio(vedio_url)
			
			elif 'covid-19' in words or 'covid' in words or 'reports' in words: covid.display_data(" ".join(words))
			
			elif 'rest' in text or 'sleep' in text: break

			else:
				name = '+'.join(words[1:])
				answer = f.get_speech(name)
				print(answer)
				speech(answer)
				#speech(wikipedia.summary(name,sentences=3))
				continue
			response()
		else:
			continue