#!/icx/software/python/bin/python

from __future__ import print_function
from __future__ import absolute_import
import argparse

from unidecode import unidecode

import _config
from ICXUtils import *
from FoodDB import DB
from django.conf import settings

db = DB()
IMAGES = settings.IMAGES_ROOT

root = '/weka/FOOD/crawller'

def init_crawler_dir(root,name,kw):
    dirname = unidecode(name.lower())
    path = root + "/"+ dirname
    print(path)
    make_path(path)

    txt = s("{path}/c.txt")
    if os.path.exists(txt):
        return

    print(txt)
   
    f = open(txt,"w");
    
    for w in kw:
        w = re.sub("_"," ",w)
        f.write(w.encode('utf-8'))
        f.write("\n");
    f.close()


parser = argparse.ArgumentParser()
#parser.add_argument("--urls", "-i", required=True)
parser.add_argument("--root","-d",default=root)
parser.add_argument("--ids",nargs="*")
parser.add_argument("--min",type=int)
Input = parser.parse_args()
root = Input.root
make_path(root)

if Input.min>0:
    fids = []
    for fid in db.select_as_column('select fid from food where not bad' ):
        count = 0
        dirs = db.select_as_column("select dataset||'/'||category_id from dataset_categories where fid=%s",[fid])
        for dir in dirs:
            try:
                count += len(ls(IMAGES+dir))
            except:
                pass

        print(fid,count,Input.min)
        if count < Input.min:
            print(fid,count,Input.min,dirs)
            fids.append(fid)
else:
    fids = Input.ids

for fid in fids:
    name  = db.select_as_value('select name from food where fid=%s',[fid])
    print("\n",fid,name)
    kw    = db.select_as_column("select distinct name from food_names where fid=%s  ",[fid])
    init_crawler_dir(root,name,kw)
