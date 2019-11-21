import json
from scrapy.http import HtmlResponse
import requests
import codecs
errors = []
resepis = []

def createUrls():
	dic = []
	sum=0
	baseUrl= "http://www.foodista.com/browse/recipes?page="
	for i in range(0,279):
		url = "%s%d"%(baseUrl,0)
		r = requests.get(url)
		response = HtmlResponse(url=url, body=r.text,encoding='utf-8')
		urlArr = response.selector.css('.views-row a::attr(href)').extract()
		dic.extend(urlArr)
		sum+= len(urlArr)
		print("sum of links: %d"%(sum))
	f = open("English_recipes\\foodista\\directorisList.txt","w+")
	f.write(json.dumps(dic))
	f.close()
	return dic

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

def step1_getDirList():
	"""
	Output: list of all directotis
	"""
	f = open("directorisList.txt","r")
	ls = f.read()
	f.close()
	ls = json.loads(ls)
	return ls

def step2_makeResepisList(a,errors=[],resepis=[]):
	"""
	Input: directotis list in a, errors list and resepis list
	Process: actual crawl, make resepis list and errors list
	"""	
	i=0
	url =""
	for link in a:
		try:
			if "http" in link:
				url = link
			else:
				url = "http://www.foodista.com%s"%(link)
			print("url: %s"%(url))
			req = requests.get(url)
			response = HtmlResponse(url=url, body=req.text,encoding='utf-8')
			subArr = response.selector.css('#block-system-main .inside .pane-node-field-rec-ing .pane-content .field-item').extract()
			resList = []
			for valu in subArr:
				subRes = HtmlResponse(url=url, body=valu,encoding='utf-8')
				textI = ' '.join(subRes.css("*::text").extract())
				while '  ' in  textI:
					textI = textI.replace("  "," ")
				if ":" in textI:
					textI = textI[textI.index(":")+1:]					
					if not textI.replace(" ","") == "":
						resList.append(textI)
				else:
					resList.append(textI)			
			title = response.selector.css('title::text').extract()[0]
			title = title.replace("Foodista | Recipes, Cooking Tips, and Food News | ","")
			img = response.selector.css('.field-items img::attr(src)').extract()
			if len(img)==0 or "recipe_big" in img[0]:
				img = ""
			else:
				img = img[0]
			newResepis={"name":title,"link":url,'img':img,"Ingredients":resList}	             
			resepis.append(newResepis)
			printFromNewResepis(newResepis,i)
			i+=1
		except:
			print(("############\nError with: %s\n##################")%(url))
			errors.append(url)

def step3_addResepiseList(resepis):
	f = codecs.open("recipesUp2.json", "a+", "utf-8")
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
	with open('recipesUp2.json', 'wb') as f:
		f.write(newRes.encode('utf-8'))
		f.close()

def main():
    a = step1_getDirList()    
    step2_makeResepisList(a,errors,resepis)
    step3_addResepiseList(resepis)
    print("############################################### END ############################################")
