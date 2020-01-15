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

logging.basicConfig(level=logging.INFO, format= '%(asctime)-15s   %(levelname)s   %(message)s')

def validate_args_and_configure_django():
    if not args.db:
        args.db = 'prod'
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
parser.add_argument('--db', help='Choose which db to read from and potentially write to. If choosing "other", you can specify the server hostname/ip via the --local_db_server parameter. But port/db/user/password should conform to the values used in other db type choices', choices=['prod', 'test', 'dev', 'other'])
parser.add_argument('--local_db_server', help='Set this if using db_type="other"')

args = parser.parse_args()

for l in ['/lib', '/ui']:
    sys.path.append(os.environ['FOODDB_ROOT'] + l)

validate_args_and_configure_django()

from food.models import *
from food.fooddb_queries import *
#END BASE SCRIPT

print("Hello World")