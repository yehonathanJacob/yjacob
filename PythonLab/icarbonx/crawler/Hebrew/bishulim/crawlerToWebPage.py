import json
import codecs

from scrapy.http import HtmlResponse
import requests

errors = []
resepis = []


def createUrls(listmain, setList={' '}):
	sum = 0
	headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.0; WOW64; rv:24.0) Gecko/20100101 Firefox/24.0'}
	for base in listmain:
		basURL = base
		con = 1
		while not con == 0:
			url = "%s?page=%d" % (basURL, con)
			try:
				r = requests.get(url, headers=headers)
				response = HtmlResponse(url=url, body=r.text, encoding='utf-8')
				check = response.selector.css('.view-empty-default').extract()
				if len(check) == 0:
					linkArr = response.selector.css('.view-content .views-row a.recipe-link::attr(href)').extract()
					for link in linkArr:
						setList.add("https://www.bishulim.co.il%s" % (link))
					sum += len(linkArr)
					print("sum of link: %d" % (sum))
					con += 1
				else:
					print("## End link: %s" % (basURL))
					con = 0
			except:
				print("Error in url: %s" % (url))
				errors.append(url)
	print("## End ##")


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


def step1_getDirList():
	"""
	Output: list of all directotis
	"""
	f = open("directorisList.txt", "r")
	ls = f.read()
	ls = json.loads(ls)
	return ls


def step2_makeResepisList(a, errors=[], resepis=[]):
	"""
	Input: directotis list in a, errors list and resepis list
	Process: actual crawl, make resepis list and errors list
	"""
	i = 0
	for link in a:
		try:
			url = link
			req = requests.get(url)
			response = HtmlResponse(url=url, body=req.text, encoding='utf-8')
			resepisDic = response.selector.css('head script[type="application/ld+json"]::text').extract()[0]
			resepisDic = json.loads(resepisDic)
			resList = resepisDic['recipeIngredient']
			if 'image' in resepisDic.keys():
				img = "https://www.bishulim.co.il%s" % (resepisDic['image'])
			else:
				img = ""
			title = resepisDic['name']
			'''textArr = response.selector.css('#recipe-full-details noscript').extract()[0]
			subRes = HtmlResponse(url=url, body=textArr,encoding='utf-8')
			subTextArr = subRes.selector.css('li::text').extract()
			resList = []
			for textI in subTextArr:				
				resList.append(textI)				
			title = response.selector.css('title::text').extract()[0]			
			img = response.selector.css('.field-items img::attr(src)').extract()
			if len(img)=0 or img[0] == "http://cloud.foodista.com/content/misc/placeholders/recipe_big":
				img = ""
			else:
				img = img[0]
			'''
			newResepis = {"name": title, "link": link, 'img': img, "Ingredients": resList}
			resepis.append(newResepis)
			printFromNewResepis(newResepis, i)
			i += 1
		except:
			print(("############\nError with: %s\n##################") % (link))
			errors.append(link)


def step3_addResepiseList(resepis):
	f = codecs.open("recipesUp1.txt", "a+", "utf-8")
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
	with open('recipesUp1.txt', 'wb') as f:
		f.write(newRes.encode('utf-8'))
		f.close()


def main():
	a = step1_getDirList()
	step2_makeResepisList(a, errors, resepis)
	step3_addResepiseList(resepis)
	print("############################################### END ############################################")
