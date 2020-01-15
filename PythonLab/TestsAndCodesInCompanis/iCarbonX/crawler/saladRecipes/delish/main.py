import json
from scrapy.http import HtmlResponse
import requests
import codecs
errors = []
resepis = []

def getListDir():
	f=open("directories_list.json","r+")
	a = f.read()
	f.close()
	a=json.loads(a)
	return a[0]['arr']

def getAllResipis(listDir):
	i=0
	for link in listDir:
		try:
			url = link
			r = requests.get(url)
			response = HtmlResponse(url=url, body=r.text,encoding='utf-8')
			ingList = response.selector.css('.ingredients-body .ingredient-lists .ingredient-item').extract()
			resList=[]
			for val in ingList:
				subRes = HtmlResponse(url=url, body=val,encoding='utf-8')
				tx = ''.join(subRes.selector.css('*::text').extract())
				while '\t' in tx:
					tx = tx.replace('\t','')
				while '\n' in tx:
					tx = tx.replace('\n','')
				resList.append(tx)
			img = response.selector.css('.recipe-body .content-lede-image .content-lede-image-wrap img::attr(data-src)').extract()
			if len(img)>0:
				img = img[0]
			else:
				img=""
			title = response.selector.css('.content-header-inner .content-hed::text').extract()[0]
			newResepis={"name":title,"link":url,'img':img,"Ingredients":resList}
			resepis.append(newResepis)
			printFromNewResepis(newResepis,i)
			i+=1
		except Exception as e:
			errors.append(link)
			print("########## Error with: %s\nresponse:%s"%(link,e))

def step3_addResepiseList(resepis):
	f = codecs.open("recipes.json", "a+", "utf-8")
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
	with open('recipes.json', 'wb') as f:
		f.write(newRes.encode('utf-8'))
		f.close()
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

def getData():
	f = codecs.open("recipes.json", "a+", "utf-8")
	f.seek(0,0)
	old  = f.read()
	f.close()
	if len(old)>0:
		old = json.loads(old)
	else:
		old = []
	return old

def main():
	print("########################## START #############################")
	listDir = getListDir()
	print("listDir: %d"%(len(listDir)))
	getAllResipis(listDir)
	step3_addResepiseList(resepis)
	print("##########################  END  #############################")
