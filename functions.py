from webbrowser import open_new
from googlesearch import search
from os import listdir,system
from time import sleep
from subprocess import Popen
from selenium import webdriver
from pyautogui import click,press
from shutil import move
from requests import get
import wiki

chrome_driver = "C:/Users/gurra/OneDrive/Documents/Drivers/chromedriver"
key = ''
cipher = [chr(x) for x in range(32,123)]
#webbrowser.register('mozilla', None, webbrowser.BackgroundBrowser('/media/mohan/Study and Softwares/firefox/firefox'))

def google_search(data):
	st="https://www.google.com/search?q="+"+".join(data)
	open_new(st)

def vedio(movie_name):
	try:
		movies = listdir('F:/movies')
		vedio_songs = listdir('F:/vedio songs')
		name=' '.join(movie_name)
		for x in movies:
			if name in x.lower():
				print(x)
				Popen(['C:/Program Files/KMPlayer 64X/KMPlayer64.exe','F:/movies/'+x])
				sleep(3)
				return True
		for x in vedio_songs:
			if name in x.lower().replace(' - ',' '):
				print(x)
				Popen(['C:/Program Files/KMPlayer 64X/KMPlayer64.exe','F:/vedio songs/'+x])
				sleep(3)
				return True
	except:
		return False

def clear():
	system('cls')
	pass

def encrypt(text):
	global cipher
	global key
	if not key: wiki.get_key('Encrypte')
	encrypted_text = ''
	encrypte_key = key*(len(text)//len(key)) + key[:len(text)%len(key)]
	for x,y in zip(text,encrypte_key):
		encrypted_text += cipher[(cipher.index(x)+cipher.index(y))%91]
	return encrypted_text
	
def decrypt(encrypted_text):
	global cipher
	global key
	if not key: wiki.get_key('Decrypte')
	text = ''
	decrypte_key = key*(len(encrypted_text)//len(key)) + key[:len(encrypted_text)%len(key)]
	for x,y in zip(encrypted_text[:-1],decrypte_key):
		text += cipher[(91+cipher.index(x)-cipher.index(y))%91]
	return text

def file_search(name):
	file = open('encrypted_details.txt','r+')
	file_Lines = file.readlines()
	file.close()
	for line in file_Lines:
		decrypted_line = decrypt(line)
		if name in decrypted_line.lower():
			return decrypted_line.split()[1:]
	else:
		print("Couldn't find the contact")
		return '';

def web(name,platform='youtube'):
	name = ' '.join(name)+" "+platform
	url = ''
	search_results = search(name)
	for x in search_results:
		if 'hashtag' not in x:
			url = x
			print(url)
			open_new(x)
			click(400,400)
			break
	return url

def save(title,text,path='Desktop'):
	loc = 'C:/Users/gurra/{}/{}.txt'.format(path,title)
	file = open(loc,'w+')
	file.write(text)
	file.close()

#def application(name):
#	if name == 'text':
#		os.startfile('C:/Program Files/Sublime Text 3/sublime_text.exe')

def weather(city='nellore'):
	city=city.title()
	r = get(f'http://api.openweathermap.org/data/2.5/weather?q={city}&APPID=5dc99925506516ff8fabbc99469f49b4')
	r=r.json()
	print("City : "+r['name'])
	return str(int(r['main']['temp'])-273),str(r['weather'][0]['description'])

def get_news(query):
	if query:
		query=" ".join(query)
		print(query)
		return get(f'https://newsapi.org/v2/top-headlines?q={query}&country=in&pageSize=5&apiKey=902ed5da698b4d2b98bcf1de3385e454').json()['articles']
	else: return get(f'https://newsapi.org/v2/top-headlines?country=in&pageSize=5&apiKey=902ed5da698b4d2b98bcf1de3385e454').json()['articles']

def facebook_log():
	user,password = file_search('facebook')
	driver = webdriver.Chrome(executable_path = chrome_driver)
	driver.get('https://www.facebook.com/')
	email = driver.find_element_by_id('email')
	driver.execute_script("arguments[0].type = 'password';", email) 
	email.send_keys(user) 
	driver.find_element_by_id('pass').send_keys(password) 
	driver.find_element_by_id('u_0_b').click() 
	print("Loged in Succesfully")

def twitter_log():
	user,password = file_search('twitter')
	driver = webdriver.Chrome(executable_path = chrome_driver)
	driver.get('https://twitter.com/login')
	driver.implicitly_wait(5)
	email = driver.find_element_by_name('session[username_or_email]')
	driver.execute_script("arguments[0].type = 'password';", email) 
	email.send_keys(user)
	driver.find_element_by_name('session[password]').send_keys(password)
	driver.implicitly_wait(5)
	driver.find_element_by_xpath("//span[contains(@class,'css-901oao css-16my406 css-bfa6kz r-1qd0xha r-ad9z0x r-bcqeeo r-qvutc0')]").click()

def sendwhatmsg(phone_no, message):
	print(message)
	open_new("https://web.whatsapp.com/send?phone="+phone_no+"&text="+message.replace(' ','%20'))
	sleep(15)
	press('enter')

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
	link = f"youtube-dl -f bestvideo+bestaudio {vedio_url[32:vedio_url.index('&')]}"
	system(link)
	sleep(2)
	file_names = listdir('G:/projects/wiki/')
	for file in file_names:
		if file[-3:] == 'mkv':
			vedio_name = file
			print("Moving vedio to vedio songs folder")
			original = r'G:/projects/wiki/'+vedio_name
			target = r'F:/vedio songs/'+vedio_name
			move(original,target)
			break

"""def get_insta_twit_links(name):
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
			twit = False"""

def get_speech(question):
	url = 'https://api.wolframalpha.com/v1/spoken?appid=LUGHK6-YH5EHYEV83&i='+question+'%3f'
	return get(url).text


	






	

