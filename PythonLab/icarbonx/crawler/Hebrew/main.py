import json
from scrapy.http import HtmlResponse
import requests
import codecs
import os
errors=[]
resepis=[]

def upData():
	mainDic = []
	dic = []
	arr = os.listdir(".")
	for fold in arr:
		file = fold+"//recipesUp1.txt"		
		if not '.' in fold and os.path.isfile(file):			
			with codecs.open(file, "r+", "utf-8") as f:
				dic = f.read()
				if len(dic)>0:
					dic = json.loads(dic)
				else:
					dic = []
				f.close()
			mainDic.extend(dic)			
	newRes =json.dumps(mainDic, ensure_ascii=False)
	with open('recipesUp1.json', 'wb') as f:
		f.write(newRes.encode('utf-8'))
		f.close()

def getData():
	f = codecs.open("recipesUp1.json", "a+", "utf-8")
	f.seek(0,0)
	dic  = f.read()
	f.close()
	if len(dic)>0:
		dic = json.loads(dic)
	else:
		dic = []
	return dic

def printSinel(rs):
	"""
	Input: get a resepis in rs and index in list
	Output: print the resepis details
	"""
	print("name: "+rs['name'][::-1])
	print("link: "+rs['link'])
	print("img: "+rs['img'])
	print("Ingredients: ",end="")
	for s in rs["Ingredients"]:
		print(str(s)+" | ",end="")
	print("\n_____________________________")

def printAll(dic = []):
	"""
	Input: get all resepis as a dictionary in dic
	Output: print the resepis details
	"""
	i=0
	for a in dic:
		print("i: %d"%(i))
		printSinel(a)
		i+=1
def cleanData():
	dic = getData()
	for res in dic:
		oldIngredients = res['Ingredients']
		newIngredients = []
		for ing in oldIngredients:
			for ing2 in ing.split(','):
				for ing3 in ing2.split('+'):
					newIngredients.append(ing3)
		res['Ingredients'] = newIngredients
		resepis.append(res)
	newRes =json.dumps(resepis, ensure_ascii=False)
	with open('recipesUp1.json', 'wb') as f:
		f.write(newRes.encode('utf-8'))
		f.close()
def getApi(tx):
	"""
	Input: plain text of one ingredient
	Output: Json from Api or {} if ther is error
	"""
	url = "http://foods.icx-il.com:5000/bot_nlp/?text=%s&tz=Asia/Jerusalem"%(tx)
	res = requests.get(url)
	res = json.loads(res.text)
	arr = []
	if not('action' in res.keys() and res['action'] == 'Unrecognized'):		
		for r in res['items']:
			#print("text:%s\nr:%s"%(tx,r))
			try:
				arr.append({"fid":r['fid'],"food":r['food'],"unit_type":r['unit_type'],"weight":r['weight']})
			except:
				pass			
	return arr
def upDataWithApi():
	"""
	Processing: do errors=[] and resepis=[] with data
	"""
	i = 0
	dic = getData()

	dic = dic[:11]

	for res in dic:
		Ingredients = res['Ingredients']
		newIngredients = []
		for ing in Ingredients:
			details = getApi(ing)			
			newIngredients.append({"text":ing, "details":details})
			if not len(details) > 0:
				errors.append({"id":i,"text":ing})
		newResepis={"name":res['name'],"link":res['link'],"img":res['img'],"Ingredients":newIngredients}
		print("id: %d"%(i))
		printSinel(newResepis)
		resepis.append(newResepis)
		i+=1
def prepareFolder():
	mainDic = []
	dic = []
	arr = os.listdir(".")
	for fold in arr:
		file = fold+"//recipesUp1.txt"		
		if not '.' in fold and os.path.isfile(file):			
			with codecs.open(file, "r+", "utf-8") as f:
				dic = f.read()
				if len(dic)>0:
					dic = json.loads(dic)
				else:
					dic = []
				f.close()
			with open('%s.json'%(fold), 'wb') as f:
				newDic =json.dumps(dic, ensure_ascii=False)
				f.write(newDic.encode('utf-8'))		
			mainDic.extend(dic)			
	newRes =json.dumps(mainDic, ensure_ascii=False)
	with open('recipesUp1.json', 'wb') as f:
		f.write(newRes.encode('utf-8'))
		f.close()
	cleanData()