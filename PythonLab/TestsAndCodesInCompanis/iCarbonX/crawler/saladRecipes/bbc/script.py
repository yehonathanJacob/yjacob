import json
import codecs

from scrapy.http import HtmlResponse
import requests

errors = []
resepis = []


def step1_getDirList():
	f = open("directoris.json", "r+")
	a = f.read()
	a = json.loads(a)
	return a


def step2_makeResepisList(a, errors=[], resepis=[]):
	i = 0
	for link in a:
		try:
			url = link
			req = requests.get(url)
			response = HtmlResponse(url=url, body=req.text, encoding='utf-8')
			ingList = response.css(
				".gel-layout__item .recipe-ingredients__list li.recipe-ingredients__list-item").extract()
			resList = []
			for li in ingList:
				subRes = HtmlResponse(url=url, body=li, encoding='utf-8')
				resList.append(''.join(subRes.css("*::text").extract()))
			title = response.selector.css('title::text').extract()[0]
			title = title.replace(" - BBC Food", "")
			img = response.css(".recipe-leading-info .gel-layout .recipe-media img::attr(src)").extract()
			if len(img) == 0:
				img = ""
			else:
				img = img[0]
			newResepis = {"name": title, "link": url, 'img': img, "Ingredients": resList}
			resepis.append(newResepis)
			printFromNewResepis(newResepis, i)
			i += 1
		except:
			print(("############\nError with: %s\n##################") % (url))
			errors.append(url)


def printFromNewResepis(rs, i=0):
	"""
	Input: get a resepis in rs and index in list
	Output: print the resepis details
	"""
	print("i: " + str(i) + " name: " + rs['name'][::-1])
	print("link: " + rs['link'])
	print("img: " + rs['img'])
	print("Ingredients: ", end="")
	for s in rs["Ingredients"]:
		print(s[::-1] + " | ", end="")
	print("\n_____________________________")


def step3_addResepiseList(resepis):
	f = codecs.open("recipesUp2.json", "a+", "utf-8")
	f.seek(0, 0)
	old = f.read()
	f.close()
	if len(old) > 0:
		old = json.loads(old)
	else:
		old = []
	for r in resepis:
		old.append(r)
	newRes = json.dumps(old, ensure_ascii=False)
	with open('recipesUp2.json', 'wb') as f:
		f.write(newRes.encode('utf-8'))
		f.close()


def main():
	a = step1_getDirList()
	step2_makeResepisList(a, errors, resepis)
	step3_addResepiseList(resepis)
	print("############################################### END ############################################")


def getData():
	f = codecs.open("bbc\\recipesUp2.json", "a+", "utf-8")
	f.seek(0, 0)
	old = f.read()
	f.close()
	if len(old) > 0:
		old = json.loads(old)
	else:
		old = []
	return old
