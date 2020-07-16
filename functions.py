import webbrowser
from googlesearch import search
import os
import time
import subprocess
import requests
from selenium import webdriver
from selenium.webdriver.support.ui import  WebDriverWait
import pyautogui as pg
import shutil
import youtube_dl
from bs4 import BeautifulSoup
import requests
import wikipedia

firefox_driver = "C:/Users/gurra/OneDrive/Documents/geckodriver"

def google_search(data):
	st="https://www.google.com/search?q="+"+".join(data)
	webbrowser.open_new(st)

def vedio(movie_name):
	movies = os.listdir('F:/movies')
	vedio_songs = os.listdir('F:/vedio songs')
	name=' '.join(movie_name)
	for x in movies:
		if name in x.lower():
			print(x)
			subprocess.Popen(['C:/Program Files/KMPlayer 64X/KMPlayer64.exe','F:/movies/'+x])
			time.sleep(10)
			return True
	for x in vedio_songs:
		if name in x.lower():
			print(x)
			subprocess.Popen(['C:/Program Files/KMPlayer 64X/KMPlayer64.exe','F:/vedio songs/'+x])
			time.sleep(10)
			return True
	return False

def clear():
    os.system( 'cls' )

def web(name,platform='youtube'):
	name = ' '.join(name)+" "+platform
	search_results = search(name)
	for x in search_results:
		if 'hashtag' not in x:
			url = x
			webbrowser.open_new(x)
#			if platform =='youtube':
#				time.sleep(3)
#				pg.click(500,500)
			break
	return url


def save(title,text,path='Desktop'):
	loc = 'C:/Users/gurra/{}/{}.txt'.format(path,title)
	file = open(loc,'w+')
	file.write(text)
	file.close()

#def site(website):
#	url = 'https://www.%s.com'%website
#	webbrowser.open_new(url)

def application(name):
	if name == 'text':
		os.startfile('C:/Program Files/Sublime Text 3/sublime_text.exe')

def weather(city='nellore'):
	city=city.title()
	r = requests.get('http://api.openweathermap.org/data/2.5/weather?q={}&APPID=5dc99925506516ff8fabbc99469f49b4'.format(city))
	r=r.json()
	print("City : "+r['name'])
	return str(int(r['main']['temp'])-273),str(r['weather'][0]['description'])

def facebook_log():
	driver = webdriver.Firefox(executable_path = firefox_driver)
	driver.get('https://www.facebook.com/') 
	driver.find_element_by_id('email').send_keys('9640505949') 
	driver.find_element_by_id('pass').send_keys('9010Amma') 
	driver.find_element_by_id('u_0_b').click() 
	print("Loged in Succesfully")
	return 0

def twitter_log():
	driver = webdriver.Firefox(executable_path = firefox_driver)
	driver.get('https://twitter.com/login')
	driver.implicitly_wait(5)
	driver.find_element_by_name('session[username_or_email]').send_keys('9182864266')
	driver.find_element_by_name('session[password]').send_keys('9010Amma')
	driver.implicitly_wait(5)
	driver.find_element_by_xpath("//span[contains(@class,'css-901oao css-16my406 css-bfa6kz r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')]").click()

def sendwhatmsg(phone_no, message):
	webbrowser.open('https://web.whatsapp.com/send?phone='+phone_no+'&text='+message)
	time.sleep(12)
	pg.press('enter')

def search_contact(contact_name):
	with open('contacts.txt') as contacts:
		contact_details = ['']
		try:
			while contact_details[0] != contact_name:
				contact_details = contacts.readline().split()
		except:
			print("No contact found")
			return 0
	return contact_details[-1]

def download_youtube_vedio(vedio_url):
	ydl_opts = {}
	with youtube_dl.YoutubeDL(ydl_opts) as ydl:
		ydl.download([vedio_url])
	file_names = os.listdir('C:/Users/gurra/AppData/Local/Programs/Python/Python35/')
	for file in file_names:
		if file[-3:] == 'mp4':
			vedio_name = file
			break
	print("Moving vedio to vedio songs folder")
	original = r"C:/Users/gurra/AppData/Local/Programs/Python/Python35/"+vedio_name
	target = r'F:/vedio songs/'+vedio_name
	shutil.move(original,target)

def get_insta_twit_links(name):
	name = name.replace(' ','+')
	url = "https://www.google.com/search?q="+name
	data = requests.get(url,headers={'User-Agent': 'Mozilla/76.0 (Macintosh; Intel Mac OS X 10_12_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.116 Safari/537.36'})
	soup = BeautifulSoup(data.content,"html.parser")
	insta,twit = True,True
	for a in soup.find_all('a',href=True):
		link = a['href']
		if ('instagram' in link) and insta and len(link)<60:
			webbrowser.open(link)
			insta = False

		if ('twitter' in link) and twit and len(link)<60:
			webbrowser.open(link)
			twit = False

def get_wiki_link(name):
	webbrowser.open(wikipedia.page(name).url)
	

	






	
