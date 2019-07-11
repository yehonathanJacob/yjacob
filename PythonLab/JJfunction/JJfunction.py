"""
JJFunction are some function that where created and edited by Jonathan Jacob.
Those function are made for personal use.
"""
__author__ = "Yehonathan Jacob"
__copyright__ = "Copyright Yehonathan Jacob 2018"
__version__ = "28_06_2019"
__date__ = "07/10/2018"
__email__ = "janjak2411@gmail.com"

import inspect,os,sys
from io import TextIOWrapper
import json
path_to_root = os.environ['yjacob_private_root'] + "\\PythonLab\\JJFunction" #Path to root where you have your private files

def show():
	print("## array of all JJFunction: FARR")
	for i in range(0,len(FARR)):		
		print("%d:\t|%s"%(i,FARR[i].__name__))

def setInString(string="",index = 0,newChars = ""):
	"""
	Input: old string, index to add new string, new char or string to add.
	Output: string that contain old string with new chars from give index.
	"""
	print( string[:index] + newChars + string[index+1:])

def	__printRecurs(back,path):
	if os.path.exists(path) and os.path.isdir(path):
		ls = os.listdir(path)
		for s in ls:
			print(back+"├──"+s)
			if s.find('.') == -1 :
				__printRecurs(back+"│  ",path+"\\"+s)

def printDirectoris(path = "."):
	"""
	Input: path of folder
	Output: print to Output all the directoris.
	"""
	back = " "
	__printRecurs(back,path)

def moovPointerOfFile(f,index=0):
	"""
	Input: pointer to an OPEN file, index where to move as array.
	Output: set the pointer to chosen index.
	"""
	if isinstance(f, TextIOWrapper):
		length = f.seek(0,2)
		if index >= -length and index <= length:
			if index < 0:
				index += length
			f.seek(index,0)
		else:
			print("the index: "+index+"\nis not in the rigth range of -"+str(length)+" to "+length)	
	else:
		print(str(f) + " is not an open file")

def _getDirFromPath(path,name, result):	
	try:
		if len(result)>1:
			return result
		arr = os.listdir(path)		
	except:
		print("can't search in path: '"+str(path)+"'. it is not a valid folder path")
		return result
	for s in arr:
		if s.find(name) > -1:
			result.append(str(path+ "/"+s))		
		if os.path.exists(path+"/"+s) and os.path.isdir(path+"/"+s):			
			result = _getDirFromPath(path+"/"+s,name,result)
	return result

def getDir(name, path = os.getcwd(), result = []):
	"""
	Input: name of file or folde to search, path to begin from (optional),result list to enter to (optional)
	Output: list with all navigation with selected file or folder
	"""
	print("searchint from: "+str(path))	
	return _getDirFromPath(path,name,result)
def getPath():
	"""
	Output: return the path of this package
	"""
	return os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

def getMyPath():
	"""
	Output: return the path of YOUR loaction
	"""
	return os.getcwd()

def BinToDec(num):
	"""
	Input: str of unsigned binnary number
	Output: return int number
	"""
	ten = 0
	binNum = num
	i = 1	
	while not(binNum == ""):
		if binNum[-1] == "1":
			ten += i
		i*=2
		binNum = binNum[:-1]	
	return ten
def HexToDec(num):
	"""
	Input: str of unsigned hexadecimal number
	Output: return int number
	"""
	ten = 0
	binNum = num
	i = 1	
	while not(binNum == ""):
		if binNum[-1] == "1":
			ten += i
		i*=2
		binNum = binNum[:-1]	
	return ten

def DecToBin(n): 
    """
	Input: number in int
	Output: str of 32 bit- signed binnary number
	"""
    d = n
    if (n<0):    	
    	print("op: %s"%(bin(n)))
    res = ""    
    for i in range(31, -1, -1):  
        k = d >> i;        
        if (k & 1): 
            res += '1'
        else: 
            res += '0'
    return res

from tkinter import filedialog
import tkinter as tkM
def ShowFileInEnding(path,end):
	"""
	Input: path: path to specific folder, end: end of wanter to be all file (example: end=".jpg" )
	Processing: create a filder fild with all file in specific end, show it, and that revers it all back.
	"""
	if os.path.exists(path) and os.path.isdir(path):
		arr = os.listdir(path)
		directory = path  +"\\JJFolder"
		os.makedirs(directory)
		for i in range(0,len(arr),1):			
			os.rename(path+"\\"+arr[i] , directory+"\\"+arr[i]+"_"+str(i)+end)
		root = tkM.Tk()
		root.filename =  filedialog.askopenfilename(initialdir = directory,title = "JJ-ShowFileInEnding",filetypes = (("all files","*.*"),("all files","*.*")))
		for i in range(0,len(arr),1):			
			os.rename(directory+"\\"+arr[i]+"_"+str(i)+end, path+"\\"+arr[i])
		os.removedirs(directory)
		root.destroy()
	else:
		print("path: %s\nDose not exist or is not a valid folder name."%path)
import datetime
import requests
import pandas as pd
def getHebDate(day = "",month = "",year = "",city="Tel+Aviv"):
	"""
	Input: specific date OR null and you will get now.
	Output: str of 32 bit- signed binnary number
	"""
	if day != "" and month != "" and year != "":
		dNow = datetime.datetime(year, month, day)
	else:
		dNow = datetime.datetime.now()
	request = 'https://www.hebcal.com/shabbat/?'
	request += '&gy='+dNow.strftime('%Y')
	request += '&gm='+str(int(dNow.strftime('%m')))
	request += '&gd='+str(int(dNow.strftime('%d')))
	request += '&city='+str(city)
	request += '&g2h=1'
	request += '&m=40'
	request += '&cfg=json'
	r = requests.get(request)
	a = r.json()
	df = pd.DataFrame(a['items'])
	df['hebrew'] = df['hebrew'][::-1]
	return df[['category','hebrew','title']]
	s = a['title']+'\nEvents:\n'
	s += "\tHebrew\t|\tTitle\t|\tCategory\t\n"
	#s += "______________|________________|__________________\n"
	for value in a['items']:
		s += "\t\t{Hebrew}|{Title}\t\t|{Category}\t\n".format(Hebrew=value['hebrew'][::-1],Title=value['title'],Category=value['category'])
	s+= '('+dNow.strftime('%A')+', '+dNow.strftime('%B')+' '+dNow.strftime('%d')+' '+dNow.strftime('%Y')+')'
	return s
#requaier: import os
import eyed3
def changeSongs(names,files,albom,artist):
	for name, file in zip(names,files):
		af = eyed3.load(file)
		af.tag.title = name
		af.tag.album = albom
		af.tag.artist = artist
		af.tag.save()
		os.rename(file,"%s.mp3"%name)
def openAssets():
	data_path = path_to_root+"\\data.json"
	f = open(data_path)
	data = json.loads(f.read())
	f.close()
	Assets_path = data["Assets"]
	Themes_path = data["Themes"]
	os.startfile(Themes_path)
	ShowFileInEnding(Assets_path,".jpg")
FARR = [show,setInString,printDirectoris,moovPointerOfFile,getDir,getPath,getMyPath,BinToDec,HexToDec,DecToBin,ShowFileInEnding,getHebDate,changeSongs,openAssets]