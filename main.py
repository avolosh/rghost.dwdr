# -*- coding: utf-8 -*-

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib, time

def get_name_by_url(url):
	names = url.split('/')
	return names[-1]
	
def get_folder_by_name(name):#Нужные расширения, если файл не из их числа - качаем следующий
	images = ['jpg', 'jpeg', 'gif', 'png']
	texts = ['txt', 'pdf'] 
	videos = ['mp4', 'avi', 'mov']
	archives = ['rar', '7z', 'zip']
	parts = name.split('.')
	extension = parts[-1]
	if extension in images:
		return 'images/'
	if extension in texts:
		return 'texts/'
	if extension in videos:
		return 'videos/'
	if extension in archives:
		return 'archives/'
	return False

def find_size(text):
	text = text.replace('(', '')
	text = text.replace(')', '')
	text = text
	mb = 'МБ'.decode('utf-8')
	if mb  in text:
		searching = text[:2]
		searching = searching.replace('.', '')
		if int(searching) > 7:
			return False
	return True
	
def get_last_id():
	file = open('lastid.txt', 'r')
	line = file.readline()
	file.close()
	return int(line)

def update_last_id(id):
	file = open('lastid.txt', 'w')
	file.write(str(id))
	file.close()
	
def check_if_denied(text):#Фразы, которые могут попасться. Встретив их, парсер поймет, что это не 404 и пойдет дальше
	bad_phrases = ['Файл удален', 'Доступ к файлу']
	for phrase in bad_phrases:
		phrase = phrase.decode('utf-8')
		if phrase in text:
			return True
	return False
	
def main():
	driver = webdriver.Firefox()
	id = get_last_id()
	while True:
		try:
			driver.get("http://rghost.ru/"+str(id))
			elem = driver.find_element_by_class_name('download')
			print 'Got element and page'
		except:
			print 'Cannot get file. Chechk time.'
			try:
				isdenied = driver.find_element_by_id('actions')
				isdeniedtext = isdenied.text
				check_denied = check_if_denied(isdeniedtext)
				if check_denied is True:
					print 'File is denided or delited'
					id+=1
					continue
			except:
				print 'File is not denided or delited.'
				if '403' in driver.title:
					id+=1
					continue
				try:
					ispassword = driver.find_element_by_id('form_for_password')
					ispasswordtext = ispassword.text
					if ispasswordtext is not None:
						id+=1
						continue
				except:
					time.sleep(3)
					continue
		sizeof = driver.find_element_by_class_name('nowrap')
		text = sizeof.text
		size = find_size(text)
		if size is not False:
			try:
				url = elem.get_attribute("href")
			except:
				try:
					ispassword = driver.find_element_by_id('form_for_password')
					ispasswordtext = ispassword.text
					if ispasswordtext is not None:
						id+=1
						continue
				except:
					continue
			print 'Url for file is '+url
			name = get_name_by_url(url)
			folder = get_folder_by_name(name)
			name = name[-30:]
			if folder is not False:
				try:
					urllib.urlretrieve(url, "downloaded/"+folder+str(id)+'_'+name)
					print 'Downloaded file '+name
					print 'Id is '+str(id)
				except:
					pass
		else:
			print 'File is too big 3:'
		update_last_id(id)
		id+=1

		
if __name__ == '__main__': main()
