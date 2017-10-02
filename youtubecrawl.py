from __future__ import unicode_literals
import requests
from bs4 import BeautifulSoup
import youtube_dl


"""Deinition of MyLogger class used by youtube-dl to print the message status"""

class MyLogger(object):
	"""docstring for MyLogger"""
	def debug(self, msg):
		pass
	def warning(self, msg):
		pass
	def error(self, msg):
		print(msg)

""" my_hook function returns the message when the status is finished"""

def my_hook(d):
	if d['status'] == 'finished':
		print('Done downloading, now converting ... ')

""" ydl_opts is the youtube-dl optional parameters, where we have specified the filetype and quality to be downloaded. In our case it's mp3 Audio file with a quality of 192"""

ydl_opts = {
	'format': 'bestaudio/best',
	'postprocessors': [{
		'key': 'FFmpegExtractAudio',
		'preferredcodec': 'mp3',
		'preferredquality': '192',
	}],
	'logger': MyLogger(),
	'progress_hooks': [my_hook],
}

""" Execution Script Starts !"""

print("Welcome to Automatic youtube !")
user_choice = str(raw_input("Enter the video you want to search for: "))
user_choice = user_choice.lower()
user_choice_list = user_choice.split()
search_url = "https://www.youtube.com/results?search_query="
search_url = search_url + user_choice_list[0]
for i in range(1, len(user_choice_list)):
	search_url = search_url + "+" + user_choice_list[i]

page=requests.get(search_url, verify=False)
soup = BeautifulSoup(page.content, 'html.parser')
results_list = soup.find_all(class_="yt-uix-tile-link")
views_list = soup.find_all(class_="yt-lockup-meta-info")

top_views_list = []
for i in range(0,5):
	view = str(views_list[i].text)
	index = view.find("ago")
	final_view = view[index+3:len(view)-6]
	final_view = final_view.split(",")
	final_view = "".join(final_view)
	int_final_view = int(final_view)
	top_views_list.append(int_final_view)

maximum_views = max(top_views_list)
max_views_index = top_views_list.index(maximum_views)
link = results_list[max_views_index]['href']

topmost_link = "https://youtube.com" + link

page1 = requests.get(topmost_link, verify=False)
soup1 = BeautifulSoup(page1.content, 'html.parser')
video_title = soup1.find('span', class_="watch-title").text
video_title = video_title.split()
print("Title : " + ' '.join(video_title))
video_author = soup1.find(class_="yt-user-info").text
video_author = video_author.split()
print("Author : " + ' '.join(video_author))
video_views = soup1.find(class_="watch-view-count").text
video_views = video_views.split()
print("Views : " + ' '.join(video_views))
video_date = soup1.find(class_="watch-time-text").text
video_date = video_date.split()
print("Date : " + ' '.join(video_date))
with youtube_dl.YoutubeDL(ydl_opts) as ydl:
	ydl.download([topmost_link])

print("The video has been downloaded in mp3 format in your current directory !")
choice = str(raw_input("Is your video a music song ? Enter Y/y for yes and N/n for no : "))
lyrics_url = "http://search.azlyrics.com/search.php?q="
if choice == 'Y' or choice == 'y' or choice == 'Yes' or choice == 'yes' or choice == 'YES':

	user_choice_list = ' '.join(user_choice_list)

	user_choice_list = user_choice_list.replace('\'', "%27")

	user_choice_list = user_choice_list.split(" ")

	test = "+".join(user_choice_list)
	lyrics_url = lyrics_url + test

	page2 = requests.get(lyrics_url, verify=False)
	soup2 = BeautifulSoup(page2.content, 'html.parser')

	lyrics_container = soup2.find_all(class_="text-left")
	lyrics_table_container = soup2.find_all(class_="table")

	if len(lyrics_table_container) == 0:
		print("Sorry the lyrics couldn't be found")

	elif len(lyrics_table_container) == 1:
		lyrics_result_list = lyrics_container[0].find('a')
		song_lyrics_url = lyrics_result_list['href']
		page3 = requests.get(song_lyrics_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'})
		soup3 = BeautifulSoup(page3.content, 'html.parser')
		song_lyrics_container = soup3.find_all('div', class_='')
		print(song_lyrics_container[1].text)
		choice_save = str(raw_input("Do you want to save the lyrics in a text file ? Enter Y/y or N/n : "))
		if choice_save == 'Y' or choice_save == 'y':
			file_name = user_choice_list[0] + "_" + "lyrics.txt"
			text_file = open(file_name, "w")
			text_file.write(song_lyrics_container[1].text)
			text_file.close()

	else:
		lyrics_result_list = lyrics_table_container[1].find('a')
		song_lyrics_url = lyrics_result_list['href']
		page3 = requests.get(song_lyrics_url, headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.75 Safari/537.36'})
		soup3 = BeautifulSoup(page3.content, 'html.parser')
		song_lyrics_container = soup3.find_all('div', class_='')
		print(song_lyrics_container[1].text)
		choice_save = str(raw_input("Do you want to save the lyrics in a text file ? Enter Y/y or N/n : "))
		if choice_save == 'Y' or choice_save == 'y':
			file_name = user_choice_list[0] + "_" + "lyrics.txt"
			text_file = open(file_name, "w")
			text_file.write(song_lyrics_container[1].text)
			text_file.close()




