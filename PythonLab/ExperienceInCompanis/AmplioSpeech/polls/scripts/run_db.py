import os, sys
import django

sys.path.append(os.getcwd())
os.environ['DJANGO_SETTINGS_MODULE']='polls.settings'
django.setup()

from api.models import Poll, Choice

print('EXAMPLE: Poll.objects.all()')

# run by: python -i scripts/run_db.py