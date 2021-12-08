# from https://www.w3schools.com/python/python_mongodb_getstarted.asp

import pymongo

myclient = pymongo.MongoClient("mongodb://localhost:27017/")

print(f"the databases: {myclient.list_database_names()}")

selected_database = 'rh_core_db__dev'
mydb = myclient[selected_database]
print(f"the tables inside {selected_database} are: \n\t{mydb.list_collection_names()}")

selectes_table = 'EventsTable'
mycol = mydb[selectes_table]
print(f"first raw inside the table {selectes_table} is: \n\t{mycol.find_one()}")

limit = 10
print(f"The {limit} first raws inside {selectes_table}:")
for index, raw in zip(range(limit),mycol.find()):
    print(f"{index}: {raw}")

