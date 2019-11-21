import json
from scrapy.http import HtmlResponse
import requests
import codecs
errors=[]
resepis=[]

def createUrls(directotisList,listmain):
	for baseURL in listmain:
		link = baseURL
		print("get into %s sum of:%d"%(link,len(directotisList)))
		recursioToLinks(link,directotisList)

def recursioToLinks(link,directotisList):
	url = link
	r = requests.get(url)
	response = HtmlResponse(url=url, body=r.text,encoding='utf-8')
	linksArr = response.selector.css('.recipes-list .fc .event-default article a.event::attr(href)').extract()
	for i in range(len(linksArr)):
		linksArr[i] = 'https://food.walla.co.il'+linksArr[i]
	directotisList.extend(linksArr)
	print("num: %d link: %s"%(len(directotisList),str(linksArr)))
	nextPage = response.selector.css('a.icon-right::attr(href)').extract()
	if len(nextPage)>0:

		recursioToLinks(nextPage[0],directotisList)

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

def getText(textI):
	if ":" in textI:
		subTx = textI[textI.index(":")+1:]
		if "," in subTx or len(subTx)>0:
			return subTx.split(",")
		else:
			return []
	else:
		return [textI]

def step0_getMainList():
	url = "https://food.walla.co.il/allcategories"
	r = requests.get(url)
	response = HtmlResponse(url=url, body=r.text,encoding='utf-8')
	response.selector.css('title::text').extract()
	listmain = response.selector.css('.food-categories .fc .event-default a.event::attr(href)').extract()
	return listmain

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
			textArr = response.selector.css('.recipe-info .cont ul li::text').extract()
			resList = []
			for textI in textArr:
				resList.extend(getText(textI))
			title = response.selector.css('title::text').extract()[0]
			title = title.replace("מתכון:","")
			title = title.replace(" - מתכונים - וואלה! אוכל","")
			newResepis={"name":title,"link":link,"Ingredients":resList}	             
			resepis.append(newResepis)
			printFromNewResepis(newResepis,i)
			i+=1
		except:
			print(("############\nError with: %s\n##################")%(link))
			errors.append(r)

def step1_getDirList():
	"""
	Output: list of all directotis
	"""
	f = open("directorisList.txt","r")
	ls = f.read()
	ls = json.loads(ls)
	return ls

def step3_addResepiseList(resepis):
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

def main():
    a = step1_getDirList()
    step2_makeResepisList(a,errors,resepis)
    step3_addResepiseList(resepis)
    print("############################################### END ############################################")

if __name__ == '__main__':
    main()

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
		img = response.selector.css('.article-content .figure img::attr(src)').extract()
		if len(img)>0:
			img = "https:%s"%(img[0])
		else:
			img = ""

		newResepis={"name":a['name'],"link":a['link'],"img":img,"Ingredients":a['Ingredients']}	             
		resepis.append(newResepis)
		printFromNewResepis(newResepis,i)
		i+=1