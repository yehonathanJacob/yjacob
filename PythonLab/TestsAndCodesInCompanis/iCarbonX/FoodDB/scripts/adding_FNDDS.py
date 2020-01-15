#START BASE SCRIPT
"""
basic file for a script to run over the DB
example: pyhton -i basic.py --db prob
"""
__author__ = "Yehonathan Jacob"
__copyright__ = "Copyright IcarbonX-il"
__version__ = "31_07_2019"
__date__ = "04/04/2019"
__email__ = "yjacob@icx-il.com"

import argparse
import sys, os
import logging
from collections import defaultdict, namedtuple
import pandas as pd
import math

import django
import re

logging.basicConfig(level=logging.INFO, format= '%(asctime)-15s   %(levelname)s   %(message)s')

def validate_args_and_configure_django():
    if not args.db:
        args.db = 'dev'
    if args.db == 'prod':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ui.settings")
    elif args.db == 'test':
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ui.settings_test")
    elif args.db in ('dev', 'other'):
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ui.settings_dev")
        if args.db == 'other':
            if not args.local_db_server:
                parser.print_help()
                logging.error('Must set "local_db_server" parameter if using db_type="other"')
                sys.exit(1)
            logging.info('Local db server: %s', args.local_db_server)
            os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ui.settings_dev")
            os.environ.setdefault("FOODDB_POSTGRES_HOST", args.local_db_server)
    logging.info('Using db_type %s', args.db)
    django.setup()


parser = argparse.ArgumentParser()
parser.add_argument('--db', help='Choose which db to read from and potentially write to. If choosing "other", you can specify the server hostname/ip via the --local_db_server parameter. But port/db/user/password should conform to the values used in other db type choices', choices=['prod', 'test', 'dev', 'other'],default='dev')
parser.add_argument('--local_db_server', help='Set this if using db_type="other"')
parser.add_argument('--read_from_csv_file', help='csv file to write results to',default=os.path.join(os.environ['FOODDB_ROOT'],'/data/FNDDS/CleanData.tsv'))
parser.add_argument('--reset',help='add if you want to delete all the FNNDS from FoodDB')
parser.add_argument('--create',help='add if you want to add all the FNND to the FoodDB',default='True')


args = parser.parse_args()

for l in ['/lib', '/ui']:
    sys.path.append(os.environ['FOODDB_ROOT'] + l)

validate_args_and_configure_django()

from food.models import *
from food.fooddb_queries import *
#END BASE SCRIPT


class AddingFood:
    def __init__(self):
        self.data_df = pd.read_csv(args.read_from_csv_file, sep='\t', encoding='utf-8')
        self.nutrient_name_TO_id = {obj['name'].lower().replace('_','').replace('-','').replace(' ',''):obj['id'] for obj in UsdaNutrient.objects.values('name','id') }
        self.splitingChars = [',', '\\\\', ':']
        linkage = [['attyacids,totalpolyunsaturated','polyunsaturatedfat'],
                   ['22:6n3','dhaomega3'],
                   ['fiber,totaldietary','dietaryfiber'],
                   ['22:5n3','dpaomega3'],
                   ['20:5n3','epaomega3'],
                   ['sugars,total','totalsugars'],
                   ['fattyacids,totalmonounsaturated','monounsaturatedfat'],
                   ['carbohydrate','totalcarbohydrate'],
                   ['thiamin','thiaminb1'],
                   ['fattyacids,totalsaturated','saturatedfat']
                   ]
        for link in linkage:
            self.nutrient_name_TO_id[link[0]] = self.nutrient_name_TO_id[link[1]]
        self.FoodDB_Head = ['beverage','breakfast_cereals','salad','snacks','sweets','vegetable']
        self.tree = {}
        self.food_clean_names = {}

    def clean_FNNDS(self):
        if FoodNodeType.objects.filter(name='fndds').exists():
            fnt = FoodNodeType.objects.get(name='fndds')
            food_to_del = Food.objects.filter(node_type= fnt)
            food_to_del_fids = food_to_del.values_list('fid',flat=True)
            FoodNutrient.objects.filter(fid__in=food_to_del_fids).delete()
            FoodNames.objects.filter(fid__in=food_to_del_fids).delete()
            FoodHier.objects.filter(Q(fid_id__in=food_to_del_fids) | Q(parent_id__in=food_to_del_fids)).delete()
            Food.objects.filter(fid__in=food_to_del_fids).delete()
            FoodNodeType.objects.filter(name='fndds').delete()

    def add_food_name(self,fndds_name):
        clean_name = self.generate_name(fndds_name,withFndds=False)
        if clean_name not in self.food_clean_names.values():
            self.tree[fndds_name] = {'children':[],'nutrients':[]}
            self.food_clean_names[fndds_name] = clean_name
            return True
        else:
            return False

    def LAYER1(self):
        '''
        Create a tree, with one level only, that parents are from column  'WWEIA Category description'
        and child are from column 'Main food description'
        check that only no option of: node in node.children
        '''
        self.data_df.apply(lambda row: self._add_row_to_dict(row) ,axis=1)
        for parent in self.FoodDB_Head:
            self.add_food_name(parent)

    def _add_row_to_dict(self,row):
        fnnds_name = row['Main food description']
        self.add_food_name(fnnds_name)
        parent_name = row['WWEIA Category description']
        self.add_food_name(parent_name)
        for column_name, value in row.items():
            if ' (' in column_name:
                nutrient_name = column_name[:column_name.index(' (')].lower().replace('_','').replace('-','').replace(' ','')
                if nutrient_name in self.nutrient_name_TO_id:
                    nutrient_id = self.nutrient_name_TO_id[nutrient_name]
                    unit = column_name[column_name.index(' (')+2:column_name.index(')')]
                    amount = value
                    self.tree[fnnds_name]['nutrients'].append({'nutrient_id':nutrient_id,
                                                              'amount': amount,
                                                              'unit': unit,
                                                              'sd_amount': 0,
                                                              'inherited':0})
        if fnnds_name != parent_name:
            self.tree[parent_name]['children'].append(fnnds_name)

    def LAYER2(self):
        '''
        adding a new level:
        the food_fndds parent, and adding to him all the parent (that are not child also)
        '''
        list_child = []
        for node in self.tree.values():
            list_child.extend(node['children'])
        set_parent = set(self.tree.keys()) - set(list_child)
        list_parent = list(set_parent)
        root_name = 'root'
        self.add_food_name(root_name)
        self.tree[root_name]['children'] =list_parent

    def LAYER3(self):
        '''
        adding for each child, his name until first ',','\\','/',':' to parent
        :return:
        '''

        self.itterate_node_adding('root')

    def itterate_node_adding(self,parent_name):
        newNames = []
        optionalNames = []
        for child in self.tree[parent_name]['children']:
            macthGroup = re.match("([a-zA-Z0-9 ]|[(][a-zA-Z0-9 ,]*[)])*[,\\\\:]",child)
            if macthGroup:
                newName = macthGroup[0][:-1]
                if re.search("^%s\w$|^%s$"%(newName,newName), parent_name):
                    continue
                optionalNames.append(newName)
        for opName in optionalNames:
            if optionalNames.count(opName) > 2 and self.add_food_name(opName):
                newNames.append(opName)
        newNames.extend(self.tree[parent_name]['children'])
        newNames = list(set(newNames))
        self.tree[parent_name]['children'] = newNames
        for child in self.tree[parent_name]['children']:
            self.itterate_node_adding(child)

    def LAYER4(self):
        '''
        creating multy level by next recursive algo:
        for each node:
            for each child:
                check if child name is subset in index 0 of other children
                if yes:
                    take those children, and take them out from node, and put the as children of the current child.
        '''
        self.iterate_node2('root',base ="|_")

    def iterate_node2(self, parent_name,base):
        logging.info(base+"|_____{}".format(parent_name))
        listChildL1 = self.tree[parent_name]['children'].copy()
        for childL1 in self.tree[parent_name]['children']:
            if childL1 not in listChildL1:
                continue
            listChildL2 = self.tree[childL1]['children']
            sub_ls1 = listChildL1.copy()
            for childL2 in sub_ls1:
                if re.search("^%s\W+"%(childL1), childL2):
                    listChildL2.append(childL2)
                    listChildL1.remove(childL2)
            self.tree[childL1]['children'] = listChildL2
        self.tree[parent_name]['children'] = listChildL1
        for childL1 in self.tree[parent_name]['children']:
            self.iterate_node2(childL1,base+"|_____")

    def creating_db(self):
        '''
        adding all the data to FoodDB
        '''
        logging.info("  |_FoodNodeType...")
        if not FoodNodeType.objects.filter(name='fndds').exists():
            obj = FoodNodeType(name="fndds",description="define all the node that came from the FNDDS DB")
            obj.save()
        logging.info("  |_FoodNodeType V")
        node_type_fndds = FoodNodeType.objects.get(name='fndds')
        crate_foods = []
        for fndds_name in self.tree.keys():
            food_name = self.generate_name(fndds_name)
            crate_foods.append(Food(name=food_name, for_classification=False, node_type=node_type_fndds))
        logging.info("  |_Food...")
        Food.objects.bulk_create(crate_foods)
        logging.info("  |_Food V")
        logging.info("  |_dic_FoodName...")
        self.dic_FoodName_to_Fid = { obj['name']:obj['fid'] for obj in Food.objects.filter(node_type=node_type_fndds).values('fid','name') }
        logging.info("  |_dic_FoodName V")
        nutrient_line =[]
        hier_line=[]
        food_name_line=[]
        ln = Lang.objects.get(code='en')
        root_name = self.generate_name('root')
        root_fid = self.dic_FoodName_to_Fid[root_name]
        hier_line.append(FoodHier(fid_id=root_fid, parent_id=1))
        logging.info("  |_BigLoop...")
        for fndds_name, node in self.tree.items():
            parent_name = self.generate_name(fndds_name)
            parent_fid = self.dic_FoodName_to_Fid[parent_name]
            food_name_line.append(FoodNames(fid_id=parent_fid,
                                            lang_code=ln,
                                            name=fndds_name,
                                            is_primary=True,
                                            is_long=False))
            for nutrient in node['nutrients']:
                nutrient_line.append(FoodNutrient(fid_id=parent_fid,
                                                  nutrient_id=nutrient['nutrient_id'],
                                                  amount=nutrient['amount'],
                                                  sd_amount=nutrient['sd_amount'],
                                                  unit=nutrient['unit'],
                                                  inherited=nutrient['inherited']))
            for fndds_child_name in node['children']:
                child_name=self.generate_name(fndds_child_name)
                child_fid=self.dic_FoodName_to_Fid[child_name]
                hier_line.append(FoodHier(fid_id=child_fid,parent_id=parent_fid))
        logging.info("  |_BigLoop V")
        logging.info("  |_FoodNutrient...")
        FoodNutrient.objects.bulk_create(nutrient_line)
        logging.info("  |_FoodNutrient V")
        logging.info("  |_FoodHier...")
        FoodHier.objects.bulk_create(hier_line)
        logging.info("  |_FoodHier V")
        logging.info("  |_FoodNames...")
        FoodNames.objects.bulk_create(food_name_line)
        logging.info("  |_FoodNames V")

    def generate_name(self,fndds_name,withFndds = True):
        s = fndds_name.lower()
        for char in self.splitingChars:
            s = s.replace('{}'.format(char),'')
        s = s.replace(' ', '_')
        s = s +'_fndds' if withFndds else s
        return s

if __name__ == '__main__':
    addingFoodObj = AddingFood()
    logging.info('|_clean_FNNDS...')
    if args.reset == 'True':
        addingFoodObj.clean_FNNDS()
    logging.info('|_clean_FNNDS V')
    logging.info("|_LAYER1...")
    addingFoodObj.LAYER1()
    logging.info("|_LAYER1 V")
    logging.info("|_LAYER2...")
    addingFoodObj.LAYER2()
    logging.info("|_LAYER2 V")
    logging.info("|_LAYER3...")
    addingFoodObj.LAYER3()
    logging.info("|_LAYER3 V")
    logging.info("|_LAYER4...")
    addingFoodObj.LAYER4()
    logging.info("|_LAYER4 V")
    if args.create == 'True':
        logging.info("|_creating_db...")
        addingFoodObj.creating_db()
        logging.info("|_creating_db V")
        logging.info("ADDED {} ITEMS TO 'root_fndds'".format(len(addingFoodObj.tree.keys())))
