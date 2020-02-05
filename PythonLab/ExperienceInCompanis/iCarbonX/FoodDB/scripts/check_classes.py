from __future__ import print_function
from __future__ import absolute_import
import re
import requests
session = requests.Session()
import json
import pandas as pd

import _config
import FoodDB

wd = '/zzp/icx/IMAGE_DATA/PRODUCTION/setups/TRAIN/models/20180221/'
#lib/PostgreSQL.DB
db = FoodDB.DB()

class_df = pd.read_table(wd+"/classes" ,names=("class","code"))
names = class_df["class"].values
#print names

simple = db.select_as_dict("select name,fid from food_names union select replace(name,'_',' '),fid from food")
for name in names:
    #name = re.sub("[ _]+"," ",name)
    #if name not in simple:
    #    print name
    url = 'https://foods.icx-il.com/food/get_foods/?name='+name
    response = session.get(url)
    if response.status_code != 200:
        print("Missing ", name)
    else:
        data = json.loads(response.text)
        data['nutrients'] = ''
        #print name,data['allnames']['cn'].encode("utf-8")
        if 'cn' not in data['allnames'] or len(data['allnames']['cn']) < 1 :
            print(name)

    #print response.text.encode("utf-8")
    #print dir(response)
    #print name,response.status_code
