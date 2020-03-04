import os,json
from tkinter import filedialog
import tkinter as tkM

def ShowFileInEnding(path, end):
	"""
	Input: path: path to specific folder, end: end of wanter to be all file (example: end=".jpg" )
	Processing: create a filder fild with all file in specific end, show it, and that revers it all back.
	"""
	if os.path.exists(path) and os.path.isdir(path):
		arr = os.listdir(path)
		directory = path + "\\JJFolder"
		os.makedirs(directory)
		for i in range(0, len(arr), 1):
			os.rename(path + "\\" + arr[i], directory + "\\" + arr[i] + "_" + str(i) + end)
		root = tkM.Tk()
		root.filename = filedialog.askopenfilename(initialdir=directory, title="JJ-ShowFileInEnding",
												   filetypes=(("all files", "*.*"), ("all files", "*.*")))
		for i in range(0, len(arr), 1):
			os.rename(directory + "\\" + arr[i] + "_" + str(i) + end, path + "\\" + arr[i])
		os.removedirs(directory)
		root.destroy()
	else:
		print("path: %s\nDose not exist or is not a valid folder name." % path)

def openAssets():
	data_path = os.path.join(os.path.dirname(os.path.abspath( __file__ )),"config.json")
	with open(data_path) as f:
		data = json.loads(f.read())
		f.close()
	Assets_path = data["Assets"]
	Themes_path = data["Themes"]
	os.startfile(Themes_path)
	ShowFileInEnding(Assets_path, ".jpg")

if __name__ == '__main__':
	openAssets()
