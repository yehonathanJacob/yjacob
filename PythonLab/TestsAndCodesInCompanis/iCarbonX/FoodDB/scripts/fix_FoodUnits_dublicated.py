#START BASE SCRIPT
from __future__ import print_function

"""
This script is created to fix a bug that you can create dublicate FoodUnits with fid_id and unit_id
 example: python -i fix_FoodUnits_dublicated.py --db_type prod --update yes
 		  python -i fix_FoodUnits_dublicated.py --db_type prod --write_to_csv_file productionImage.tsv
"""
from builtins import input
__author__ = "Yehonathan Jacob"
__copyright__ = "Copyright IcarbonX-il"
__version__ = "17_03_2019"
__date__ = "17/03/2019"
__email__ = "yjacob@icx-il.com"

import argparse
import sys, os
import logging
from collections import defaultdict, namedtuple
import pandas as pd
import math

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
	if not args.write_to_csv_file:
		logging.warning('need specify write_to_csv_file, othewise it write to out.txt')
		args.write_to_csv_file = "out.txt"


parser = argparse.ArgumentParser()
parser.add_argument('--db_type', required=True, help='Choose which db to read from and potentially write to. If choosing "other", you can specify the server hostname/ip via the --local_db_server parameter. But port/db/user/password should conform to the values used in other db type choices', choices=['prod', 'test', 'dev', 'other'])
parser.add_argument('--local_db_server', help='Set this if using db_type="other"')
parser.add_argument('--write_to_csv_file', help='csv file to write results to')
parser.add_argument('--update', help='type "yes" if you want the data base to be updated')

args = parser.parse_args()

for l in ['/lib', '/ui']:
    sys.path.append(os.environ['FOODDB_ROOT'] + l)

validate_args_and_configure_django()

from food.models import *
from food.fooddb_queries import *
#END BASE SCRIPT

def getBadDic():
	data = list(FoodUnits.objects.all().values())
	dic = {}
	for obj in data:
		key = "[fid_id: {0}, unit_id: {1}]".format(obj['fid_id'],obj['unit_id'])
		if key not in dic:
			dic[key] = []
		dic[key].append(obj)
	arr = list(dic.keys())
	for key in arr:
		if len(dic[key]) <=1:
			dic.pop(key)
	return dic

def getData(dic):
	units = {obj['unit_id']:{'name_cn':obj['name_cn'], 'name_en':obj['name_en'], 'name_he':obj['name_he']}
			 for obj in list(Units.objects.all().values())}
	foods = {obj['fid']:obj['name'] for obj in list(Food.objects.all().values())}
	data = []
	for key in dic:
		smallList = dic[key]
		smallList = sorted(smallList, key=lambda k: k['id'])
		unit_names = units[smallList[0]['unit_id']]
		food_name = foods[smallList[0]['fid_id']]
		for obj in smallList:
			data.append({'id':obj['id'],'weight':obj['weight'],
						 'fid':obj['fid_id'], 'food_name': food_name,
						 'unit_id': obj['unit_id'],
						 'unit_en':unit_names['name_he'], 'unit_he':unit_names['name_he'], 'unit_cn':unit_names['name_cn']})
	return data

def deletBadData(dic):
	ls= []
	for key in dic:
		smallList = dic[key]
		smallList = sorted(smallList, key=lambda k: k['id'])
		for obj in smallList[:-1]:
			ls.append(obj['id'])
	i = "x"
	print('list to delete: ', ls)
	while not (i == "yes" or i == "no"):
		i = eval(input("do you want to delete all this list of ids? (yes/no)\n"))
	if i == "yes":
		FoodUnits.objects.filter(id__in = ls).delete()
		print("deleted.")

def main():
	logging.info("################## START ###################")
	logging.info("getBadDic")
	dic = getBadDic()
	logging.info("getData")
	data = getData(dic)
	logging.info("print output to: %s" % (args.write_to_csv_file))
	newdf = pd.DataFrame(data)
	if len(data)>0:
		newdf = newdf[['id', 'weight', 'fid', 'food_name', 'unit_id', 'unit_en',
				   'unit_he', 'unit_cn']]
	newdf.to_csv(args.write_to_csv_file, sep='\t', encoding='utf-8')
	if args.update and args.update == "yes":
		logging.info("going to delete: ")
		deletBadData(dic)
	logging.info("################## END ###################")

if __name__ == '__main__':
	main()