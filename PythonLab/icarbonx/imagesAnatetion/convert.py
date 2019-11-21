import json
import codecs
import os
from shutil import copyfile
import argparse
errors = []
mainList = []
workList = []

def createJsonFile(sourceFolder,targetFolder,jsonFileName):
	"""
	Input: sourceFolder = where all fikes arr. targetFolder = where to put all folder. jsonFileName = "example.json"
	Ouput: targetFolder/out.json = [{"values":[] , "images":[] }, ...]
	"""
	listOfEscape = ["unidentified","black_pepper","coriander"]
	sF = "%s/"%(sourceFolder)
	tF = "%s/"%(targetFolder)
	directoryJsonFile = "%s/%s"%(sourceFolder,jsonFileName)
	if not (os.path.exists(tF) and os.path.isdir(tF)):
		os.makedirs(tF)
	f = codecs.open(directoryJsonFile, "a+", "utf-8")
	f.seek(0,0)
	data = f.read()
	f.close()
	data = json.loads(data)	
	subList = []
	for a in data:
		try:
			subList = a['Label']['salad']
			subList = set(subList) - set(listOfEscape)
			subList = list(subList)
			for i in range(len(subList)):
				if "bread" in subList[i]:
					subList[i]= "bread"
			subList.sort()
			textList = ','.join(subList)

			if not (textList in workList):				
				workList.append(textList)
				newVal = {"salad":subList,"images":[]}
				mainList.append(newVal)
			key = workList.index(textList)
			value = mainList[key]
			value['images'].append(a['External ID'])
			mainList[key] = value
		except:
			errors.append(a)
			print("Error with: %s"%(a['ID']))
	newJson = json.dumps(mainList, ensure_ascii=False)
	with open('%s/out.json'%(tF), 'wb') as f:
		f.write(newJson.encode('utf-8'))
		f.close()

def sol1(sourceFolder,targetFolder,listOfValue = mainList,workList = workList):
	sF = "%s/"%(sourceFolder)
	tF = "%s/"%(targetFolder)
	for i in range(len(listOfValue)):		
		folder = "%s%d_%s/"%(tF,len(listOfValue[i]['images']),workList[i])
		os.makedirs(folder)
		imgArr = listOfValue[i]['images']
		for img in imgArr:
			src = "%s%s"%(sF,img)
			dst = "%s%s"%(folder,img)
			copyfile(src, dst)


parser = argparse.ArgumentParser()
parser.add_argument('--sFolder', help='sourceFolder')
parser.add_argument('--tFolder', help='targetFolder')
parser.add_argument('--jsonF', help='jsonFileName')
args = parser.parse_args()
if args.sFolder and args.tFolder and args.jsonF:
   createJsonFile(args.sFolder,args.tFolder,args.jsonF)
   sol1(args.sFolder,args.tFolder)