import json
from scrapy.http import HtmlResponse
import requests
import codecs
import os
reviews = []
errors = []

def upData():
	mainDic = []
	dic = []
	arr = os.listdir(".")
	for fold in arr:
		file = fold+"//reviews.txt"
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
	with open('reviews.json', 'wb') as f:
		f.write(newRes.encode('utf-8'))
		f.close()
def getData():
	f = codecs.open("reviews.json", "a+", "utf-8")
	f.seek(0,0)
	dic  = f.read()
	f.close()
	if len(dic)>0:
		dic = json.loads(dic)
	else:
		dic = []
	return dic

def getNum():
	dic = getData()
	wordSize = 0
	for text in dic:
		try:
			tx = text['text']
			if tx.index(" ") == 0:
				tx = tx[1:]
			if tx.rfind(" ") == 0:
				tx = tx[:-1]
			wordSize+=len(tx.split(" "))
		except:
			print("Error with: "+str(text))
	print("num reviews: %d\nnum words: %d"%(len(dic),wordSize))

def prepareFolder():
	mainDic = []
	dic = []
	arr = os.listdir(".")
	for fold in arr:
		file = fold+"//reviews.txt"		
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
	with open('reviews.json', 'wb') as f:
		f.write(newRes.encode('utf-8'))
		f.close()	