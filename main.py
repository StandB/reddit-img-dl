import praw
import config
import time
import urllib.request
import os
from bs4 import BeautifulSoup
from slugify import slugify
from imgurpython import ImgurClient

reddit = praw.Reddit(client_id=config.client_id, client_secret=config.client_secret, user_agent=config.user_agent)
reddit.read_only = True # might not be needed at all.

client = ImgurClient(config.imgur_client_id, "")

subreddits = config.subreddits

# was working on this. might just wanna use some module.
def alb_handler(url):
	alb_id = url.split("/")[4]
	imgs = client.get_album_images(alb_id)
	for x in imgs:
		temp_path = os.path.join(config.path, slugify(str(x.datetime)) + '.jpg')
		print(x.link)
		try:
			urllib.request.urlretrieve(x.link, temp_path)
		except Exception as e:
			print("Request failed: " + str(e))
			pass


count = 0

while True:
	for sub in subreddits:
		for submission in reddit.subreddit(sub).hot(limit=10):
			count += 1
			print(submission.title + " " + submission.url)

			temp_path = os.path.join(config.path, slugify(submission.title))
			url = submission.url

			if 'reddit.com/r/' in url:
				continue

			if 'reddituploads' in url and '.jpg' not in url and '.png' not in url:
				url += ".jpg"

			if 'imgur.com/a/' in url or 'imgur.com/gallery/' in url:
				alb_handler(url)
				continue

			if 'imgur' in url and '.jpg' not in url and '.png' not in url:
				url += ".jpg"

			if '.jpg' in url:
				temp_path += '.jpg'
			elif '.png' in url:
				temp_path += '.png'

			try:
				urllib.request.urlretrieve(url, temp_path)
			except Exception as e:
				print("Request failed: " + str(e))
				pass
		time.sleep(1)
	print(count)
	time.sleep(60)

