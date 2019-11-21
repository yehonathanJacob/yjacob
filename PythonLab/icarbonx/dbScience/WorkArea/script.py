import pyodbc

def get_usda_refs_Sheet1():
	conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\janjak2411\Desktop\PythonLab\icarbonx\dbScience\WorkArea\WorkArea.accdb;')
	cursor = conn.cursor()
	cursor.execute('select * from usda_refs_Sheet1')
	arr=[]
	for row in cursor.fetchall():
		arr.append({'usda name':row[1],'FoodDB name':row[5]})
	conn.close()
	return arr

def get_LANGUAL():
	conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\janjak2411\Desktop\PythonLab\icarbonx\dbScience\WorkArea\WorkArea.accdb;')
	cursor = conn.cursor()
	cursor.execute('select * from LANGUAL')
	arr=[]
	for row in cursor.fetchall():
		arr.append({'usda id':row[0],'langual tags':row[1]})
	conn.close()
	return arr

def get_LANGDESC():
	conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\janjak2411\Desktop\PythonLab\icarbonx\dbScience\WorkArea\WorkArea.accdb;')
	cursor = conn.cursor()
	cursor.execute('select * from LANGDESC')
	arr=[]
	for row in cursor.fetchall():
		arr.append({'langual tags':row[0],'langual descriptions':row[1]})
	conn.close()
	return arr

def get_FOOD_DES():
	conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\janjak2411\Desktop\PythonLab\icarbonx\dbScience\WorkArea\WorkArea.accdb;')
	cursor = conn.cursor()
	cursor.execute('select * from FOOD_DES order by NDB_No')
	arr=[]
	for row in cursor.fetchall():
		arr.append({'usda id':row[0],'usda name':row[2]})
	conn.close()
	return arr

def addDataToOutput(arr):
	conn = pyodbc.connect(r'Driver={Microsoft Access Driver (*.mdb, *.accdb)};DBQ=C:\Users\janjak2411\Desktop\PythonLab\icarbonx\dbScience\WorkArea\WorkArea.accdb;')
	cursor = conn.cursor()
	for obj in arr:
		cursor.execute("INSERT INTO [Output] ( FoodDB_name, usda_name, usda_id, langual_tags, langual_descriptions)  VALUES ('%s','%s','%s','%s','%s');"%(obj['FoodDB_name'],obj['usda_name'],obj['usda_id'],obj['langual_tags'],obj['langual_descriptions']))
	conn.commit()
	conn.close()