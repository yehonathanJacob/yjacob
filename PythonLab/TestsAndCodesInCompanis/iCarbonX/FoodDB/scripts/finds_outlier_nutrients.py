#START BASE SCRIPT
"""
This script is created to finds outlier nutrients in child info
 example: python -i finds_outlier_nutrients.py --db_type prod --nutrient_names energy moisture
"""
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
parser.add_argument('--nutrient_names', required=True, help='nutrient names to check', nargs='+')
parser.add_argument('--root', help='csv file to read results from', nargs='+')
parser.add_argument('--exclude', help='csv file to read results from', nargs='+')

args = parser.parse_args()

for l in ['/lib', '/ui']:
	sys.path.append(os.environ['FOODDB_ROOT'] + l)

validate_args_and_configure_django()

from food.models import *
from food.fooddb_queries import *
#END BASE SCRIPT

def main():
	logging.info("################## START ###################")
	runObj = finds_outlier_nutrients(nutrient_names = args.nutrient_names, root = args.root, exclude = args.exclude)
	data = runObj.run()
	newdf = pd.DataFrame(data)
	newdf = newdf[['parent_name', 'parent_fid', 'child_name', 'child_fid','child_is_representive', 'nutrient_name', 'parent_average', 'parent_standard_deviation', 'amount_of_child', 'deviation_of_child', 'distance_of_child']]
	logging.info("print output to: %s"%(args.write_to_csv_file))
	newdf.to_csv(args.write_to_csv_file, sep='\t', encoding='utf-8')
	logging.info("################## END ###################")


if __name__ == '__main__':
	main()