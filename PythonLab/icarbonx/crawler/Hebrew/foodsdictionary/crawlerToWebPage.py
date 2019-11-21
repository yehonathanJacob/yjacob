import json
from scrapy.http import HtmlResponse
import requests
import codecs
errors = []
resepis = []

def createUrls(directotisList,listmain):
	for baseURL in listmain:
		url = baseURL
		r = requests.get(url)
		response = HtmlResponse(url=url, body=r.text,encoding='utf-8')
		subArr = response.selector.css('.clickableContainer .LinkRedHP::attr(href)').extract()
		directotisList.extend(subArr)

def getTextFromLi(li):
	response = HtmlResponse(url="", body=li,encoding='utf-8')
	name = ' '.join(response.selector.css('span a *::text').extract())
	amount = ' '.join(response.selector.css('span[property="v:amount"]::text').extract())
	amount = amount.replace(" ","")
	amount = amount.replace(" - ","")
	return "%s %s"%(name,amount)

def printFromNewResepis(rs,i=0):
	"""
	Input: get a resepis in rs and index in list
	Output: print the resepis details
	"""
	print("i: "+str(i)+" name: "+rs['name'][::-1])
	print("link: "+rs['link'])
	print("img: "+rs['img'])
	print("Ingredients: ",end="")
	for s in rs["Ingredients"]:
		print(s[::-1]+" | ",end="")
	print("\n_____________________________")

def addResepiseList(resepise2):
	f = codecs.open("recipesUp1.txt", "a+", "utf-8")
	f.seek(0,0)
	old  = f.read()
	f.close()
	if len(old)>0:
		old = json.loads(old)
	else:
		old = []
	for r in resepis:
		old.append(r)
	newRes =json.dumps(old, ensure_ascii=False)
	with open('recipesUp1.txt', 'wb') as f:
		f.write(newRes.encode('utf-8'))
		f.close()

def step1_getDirList():
	"""
	Output: list of all directotis
	"""
	f = open("directorisList.txt","r")
	ls = f.read()
	ls = json.loads(ls)
	return ls

def step2_makeResepisList(a,errors=[],resepis=[]):
	"""
	Input: directotis list in a, errors list and resepis list
	Process: actual crawl, make resepis list and errors list
	"""	
	i=0
	for link in a:
		try:
			url = link
			req = requests.get(url)
			response = HtmlResponse(url=url, body=req.text,encoding='utf-8')
			liArr = response.selector.css('.recipe-ingredients li:not(.sub-title)').extract()
			resList = []			
			for li in liArr:
				text = getTextFromLi(li)
				li = HtmlResponse(url=url, body=text,encoding='utf-8')				
				resList.append(text)
			title = response.selector.css('title::text').extract()[0]
			title = title.replace("FoodsDictionary -","")
			title = title.replace(" - מתכון","")
			newResepis={"name":title,"link":link,"Ingredients":resList}	             
			resepis.append(newResepis)
			printFromNewResepis(newResepis,i)
			i+=1
		except:
			print(("############\nError with: %s\n##################")%(link))
			errors.append(link)
def getData():
	f = codecs.open("recipes_UTF8.txt", "a+", "utf-8")
	f.seek(0,0)
	DB  = f.read()
	f.close()
	if len(DB)>0:
		DB = json.loads(DB)
	else:
		DB = []
	return DB

def upDateDat(dic):
	i=0	
	for a in dic:
		url = a['link']
		r = requests.get(url)
		response = HtmlResponse(url=url, body=r.text,encoding='utf-8')
		img = response.selector.css('#weekRecipePic0 img::attr(src)').extract()[0]
		newResepis={"name":a['name'],"link":a['link'],"img":img,"Ingredients":a['Ingredients']}	             
		resepis.append(newResepis)
		printFromNewResepis(newResepis,i)
		i+=1