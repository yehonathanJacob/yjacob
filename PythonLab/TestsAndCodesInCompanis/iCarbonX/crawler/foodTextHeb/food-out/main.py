import json
import codecs

from scrapy.http import HtmlResponse
import requests

reviews = []
errors = []


def getDirectooris():
	f = open("directoris.txt", "r+")
	links = f.read()
	f.close()
	links = json.loads(links)
	return links


def getAllReviwes(dirList):
	lenText = 0
	for link in dirList:
		url = link
		res = requests.get(url)
		response = HtmlResponse(url=url, body=res.text, encoding='utf-8')
		try:
			text = ' '.join(response.css(".post-body div div::text").extract())
			while '  ' in text:
				text = text.replace('  ', ' ')
			reviews.append({"link": link, "text": text})
			lenText += len(text)
			print("len of all text:%d" % (lenText))
		except:
			errors.append({"link": link, "response": response})
			print("###################Errors with: %s########" % (link))


def addReviwesList(reviews):
	f = codecs.open("reviews.txt", "a+", "utf-8")
	f.seek(0, 0)
	old = f.read()
	f.close()
	if len(old) > 0:
		old = json.loads(old)
	else:
		old = []
	for r in reviews:
		old.append(r)
	newRes = json.dumps(old, ensure_ascii=False)
	with open('reviews.txt', 'wb') as f:
		f.write(newRes.encode('utf-8'))
		f.close()


def getData():
	f = codecs.open("reviews.txt", "a+", "utf-8")
	f.seek(0, 0)
	DB = f.read()
	f.close()
	if len(DB) > 0:
		DB = json.loads(DB)
	else:
		DB = []
	return DB
