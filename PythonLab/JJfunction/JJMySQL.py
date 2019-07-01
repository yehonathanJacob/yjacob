"""
JJMySQL is a python module for hendelling with MySQL connction and SQL query.
This module created and edited by Jonathan Jacob.
Those function are made for personal use.
"""
__author__ = "Yehonathan Jacob"
__copyright__ = "Copyright Yehonathan Jacob 2018"
__version__ = "08_12_2018"
__date__ = "26/11/2018"
__email__ = "janjak2411@gmail.com"

import mysql.connector
from mysql.connector import Error
import json
import sys,inspect,os

path_to_root = os.environ['yjacob_private_root'] + "\\PythonLab\\JJMySQL" #Path to root where you have your private files
#os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))

def runQuery(connection = {"host":"", "user":"", "passwd":"", "database":""}, QUERY = ""):
	"""
	Input: obecjt filled with details for MySQL connection, SQL- QUERY.
	Output: QUERY result or an error otherwise.
	"""
	try:
		conn = mysql.connector.connect(
			host		= connection["host"],
			user		= connection["user"],
			passwd		= connection["passwd"],
			database	= connection["database"]
		)		
		if conn.is_connected():			
			mycursor  = conn.cursor()			
			mycursor.execute(QUERY)	
			results = mycursor.fetchall()			
			return results
		else:
			return "Error in details connection."
	except Error as e:
		return str(e)
	finally:
		conn.close()
def runInsert(connection = {"host":"", "user":"", "passwd":"", "database":""}, QUERY = "",VAL = ""):
	"""
	Input: obecjt filled with details for MySQL connection, SQL- QUERY, SQL-VAL.
	Output: num of inserted row.
	"""
	try:
		conn = mysql.connector.connect(
			host		= connection["host"],
			user		= connection["user"],
			passwd		= connection["passwd"],
			database	= connection["database"]
		)		
		if conn.is_connected():			
			mycursor  = conn.cursor()			
			mycursor.executemany(QUERY,VAL)			
			conn.commit()			
			results = mycursor.rowcount
			return results
		else:
			return "Error in details connection."
	except Error as e:
		return str(e)
	finally:
		conn.close()
def getConnections():
	"""	
	Output: dictionery filled with all connection details.
	"""
	x = path_to_root + "\\sqlconnection.txt"
	f = open(x)
	x = json.loads(f.read())
	f.close()
	return x
def showConnections():
	"""	
	Output: print all Connection details avalibel
	"""
	x = path_to_root + "\\sqlconnection.txt"
	f = open(x)
	x = json.loads(f.read())
	f.close()
	flag = 0
	for i in x:
		if flag:
			print("________________________________________________")
		else:
			print("ALL CONNECTION DETALIS:")
			flag = 1
		print("Name:\t\t%s"%(str(i)))
		print("host:\t\t%s"%(str(x[i]['host'])))
		print("user:\t\t%s"%(str(x[i]['user'])))
		print("passwd:\t\t%s"%(str(x[i]['passwd'])))
		print("database:\t%s"%(str(x[i]['database'])))
def editConnection():
	"""	
	Processing: get all details of a connection, and set it in data If it exist- destroy and create new one, else- create new one.
	"""
	print("Name: ",end = "")
	name = input()
	print("host: ",end = "")
	host = input()
	print("user: ",end = "")
	user = input()
	print("passwd: ",end = "")
	passwd = input()
	print("database: ",end = "")
	database = input()

	path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "\\sqlconnection.txt"
	f = open(path)
	x = json.loads(f.read())
	f.close()
	x[name] = {'host':host,'user':user,'passwd':passwd,'database':database}
	f = open(path, "w")
	f.write(json.dumps(x))
	f.close()
	print("Saved.")
def deleteConnection():
	"""	
	Processing: get name of a connection, and delete it.
	"""
	print("Name: ",end = "")
	name = input()

	path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe()))) + "\\sqlconnection.txt"
	f = open(path)
	x = json.loads(f.read())
	f.close()
	del x[name]
	f = open(path, "w")
	f.write(json.dumps(x))
	f.close()
	print("Deleted.")