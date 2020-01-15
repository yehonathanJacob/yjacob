"""
This script is created to update the food_attributes table using:
 tables: food, food_attribute, food_attributename, food_attributes, food_names
 function: foods_for
 example: python attr_id_AND_fid.py --db_type prod --type_id 2 --write_to_csv_file out.txt --only_new
          python attr_id_AND_fid.py --db_type prod --type_name dietary_info --write_to_csv_file attr_id_AND_fid1.tsv --only_new yes --excluding To_delete.tsv
"""
__author__ = "Yehonathan Jacob"
__copyright__ = "Copyright IcarbonX-il"
__version__ = "17_02_2019"
__date__ = "17/02/2019"
__email__ = "yjacob@icx-il.com"

import argparse
import sys, os
import logging
from collections import defaultdict, namedtuple
import pandas as pd
import codecs
import django

logging.basicConfig(level=logging.INFO, format= '%(asctime)-15s   %(levelname)s   %(message)s')

def validate_args_and_configure_django():
    if args.db_type == 'prod':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ui.settings")
    elif args.db_type == 'test':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ui.settings_test")
    elif args.db_type in ('dev', 'other'):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ui.settings_dev")
        if args.db_type == 'other':
            if not args.local_db_server:
                parser.print_help()
                logging.error('Must set "local_db_server" parameter if using db_type="other"')
                sys.exit(1)
            logging.info('Local db server: %s', args.local_db_server)
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ui.settings_dev")
            os.environ.setdefault("FOODDB_POSTGRES_HOST", args.local_db_server)
    logging.info('Using db_type %s', args.db_type)
    django.setup()

parser = argparse.ArgumentParser()
parser.add_argument('--db_type', required=True, help='Choose which db to read from and potentially write to. If choosing "other", you can specify the server hostname/ip via the --local_db_server parameter. But port/db/user/password should conform to the values used in other db type choices', choices=['prod', 'test', 'dev', 'other'])
parser.add_argument('--local_db_server', help='Set this if using db_type="other"')
parser.add_argument('--write_to_csv_file', help='csv file to write results to')
parser.add_argument('--read_from_csv_file', help='csv file to read results from')
parser.add_argument('--type_id', type = int, help='type_id fillter or -1 for all')
parser.add_argument('--type_name', type = str, help='type_name fillter or -1 for all')
parser.add_argument('--only_new', help='edit when want to have only new connections')
parser.add_argument('--excluding', help='csv file to exclud results from')

args = parser.parse_args()

for l in ['/lib', '/ui']:
    sys.path.append(os.environ['FOODDB_ROOT'] + l)

validate_args_and_configure_django()

from food.models import *
from food.fooddb_queries import *

def get_all_attribute_rellevent_name(type_id = -1):
    """
    Input: optional: type_id of relevent attributes, defult -1 for all of them
    Output: [{ "id":atrr_id, "names": [], "value": "", "type_id": -1}, ]
    """
    dbList = []
    if type_id == -1:
        dbList = Attribute.objects.all()
    else:
        dbList = Attribute.objects.filter(type_id = type_id)
    db = []
    ls = []
    for obj in dbList:
        if obj.id in ls:
            logging.error('id: %d id twice in food_attribute, taken only one')
            sys.exit(1)
        else:
            ls.append(obj.id)
            db.append({"id":obj.id, "names":[obj.value], "value":obj.value, "type_id":obj.type_id})
    dbList = AttributeName.objects.all()
    for obj in dbList:
        if obj.attribute_id in ls:
            i = ls.index(obj.attribute_id)
            db[i]["names"].append(obj.name)
    return db

def save_all_attribute_rellevent_name(backData = None):
    """
    Output: print to csv file the output of get_all_attribute_rellevent_name
    :return: DataFrame with saved data
    """
    if args.type_id is None:
        logging.warning('should have "type_id" parameter if using this function, otherwise it brings all')
        args.type_id = -1
    db = get_all_attribute_rellevent_name(args.type_id)

    #createCSV from db
    listToFile1 = []
    for obj in db:
        listToFile1.append({'id':obj['id'],'names':'#'.join(obj['names']), 'value':obj['value'], 'type_id':obj['type_id']})
    df = pd.DataFrame(listToFile1)
    if args.write_to_csv_file is None:
        logging.warning('should have "write_to_csv_file" parameter if using this function, otherwise it the file output id "out.txt"')
        args.write_to_csv_file = "out.txt"
    df.to_csv(args.write_to_csv_file, sep='\t', encoding='utf-8')
    logging.info("data saved in: %s" % (args.write_to_csv_file))

    return df

def get_comper_fid_TO_attr_id(backData = None):
    """
    Output: [{ "fid": food.fid, "food_name": food.name, "attr_name": AttributeName.name , "attr_id": Attribute.id, "type_id": -1}, ]
    """
    data = []
    if not backData is None:
        data = backData
        data = list(data.T.to_dict().values())
    elif args.read_from_csv_file:
        data = pd.read_csv(args.read_from_csv_file, sep='\t')
        data = list(data.T.to_dict().values())
    else:
        logging.warning('should have "read_from_csv_file" parameter if using this function, otherwise the it get data from get_all_attribute_rellevent_name\nhint: call first "save_all_attribute_rellevent_name"')
        if not args.type_id:
            logging.warning('should have "type_id" parameter if using this function, otherwise it brings all')
            args.type_id = -1
        data = get_all_attribute_rellevent_name(type_id = args.type_id)
    old = data
    data = []
    for obj in old:
        data.append({"attr_id":obj["id"], "attr_name":obj["value"], "type_id":obj["type_id"], "names": obj["names"].split("#")})
    old = data
    data=[]
    # reload(sys)
    # sys.setdefaultencoding('utf8')
    logging.info("working on attribute")
    for obj in old:
        logging.info("|-working on attr: %s"%(obj["attr_name"]))
        fids = []
        foods = []
        for name in obj["names"]:
            logging.info("|\t|-working on name: %s" % (name))
            fid_list = foods_for(name, asSubstring = False)
            for obj2 in fid_list:
                if not(obj2["f"].fid in fids):
                    fids.append(obj2["f"].fid)
                    foods.append({"fid": obj2["f"].fid, "food_name": obj2["f"].name})
        data.append({"attr_id":obj["attr_id"], "attr_name":obj["attr_name"], "type_id":obj["type_id"], "foods": foods})

    #exclud old data and 'args.excluding' data
    old = data
    data = []
    dfEx = df = pd.DataFrame(columns=['fid', 'attr_id'])
    if args.excluding: # exclud file must have [fid,attr_id]
        dfEx = pd.read_csv(args.excluding, sep='\t', encoding='utf-8')
        for col in ('fid', 'attr_id'): # check excluding file
            if col not in dfEx.columns:
                logging.error('Csv file does not have a "%s" column. Columns found: %s', col, dfEx.columns)
                sys.exit(2)
    FA = FoodAttributes.objects.all()
    for obj in old:
        for food in obj["foods"]:
            if (not args.only_new) or (not FA.filter(fid_id=food["fid"], attr_id=obj["attr_id"])) and not ((dfEx['fid'] == food["fid"]) & (dfEx['attr_id'] == obj["attr_id"])).any():
                data.append({"fid": food["fid"], "food_name": food['food_name'], "attr_name": obj["attr_name"], "attr_id": obj["attr_id"], "type_id":obj["type_id"]})
    return data

def save_comper_fid_TO_attr_id(backData = None):
    """
    Input: File address to read data from, file address to write data to.
    Output: print to csv file the output of get_comper_fid_TO_attr_id
    :param backData: DataFrame that contain all_attribute_rellevent_name
    :return: DataFrame with saved data
    """
    data = get_comper_fid_TO_attr_id(backData = backData)
    df = pd.DataFrame(data)
    if args.write_to_csv_file is None:
        logging.warning('should have "write_to_csv_file" parameter if using this function, otherwise it the file output id "out.txt"')
        args.write_to_csv_file = "out.txt"
    df.to_csv(args.write_to_csv_file, sep='\t', encoding='utf-8')
    logging.info("data saved in: %s" % (args.write_to_csv_file))
    return df


def main():

    if args.excluding:  # exclud file must have [fid,attr_id]
        args.excluding= pd.read_csv(args.excluding, sep='\t', encoding='utf-8')
    logging.info("################## START ###################")
    runObj = attr_id_AND_fid(True,type_id=args.type_id, type_name=args.type_name,
                             only_new = args.only_new, excluding = args.excluding)
    data = runObj.run()
    df = pd.DataFrame(data)
    if args.write_to_csv_file is None:
        logging.warning('should have "write_to_csv_file" parameter if using this function, otherwise it the file output id "out.txt"')
        args.write_to_csv_file = "out.txt"
    df.to_csv(args.write_to_csv_file, sep='\t', encoding='utf-8')
    logging.info("data saved in: %s" % (args.write_to_csv_file))
    logging.info("################## END ###################")

    return data

if __name__ == '__main__':
    main()
