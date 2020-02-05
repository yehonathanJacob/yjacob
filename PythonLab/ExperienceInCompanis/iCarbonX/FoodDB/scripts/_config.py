import sys,os
_libs = ["/lib/python","/lib","/ui"]
for l in _libs:
    sys.path.append(os.environ['FOODDB_ROOT']+l)

import logging
logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
import PIL
logging.basicConfig(level=logging.DEBUG, format="%(asctime)-15s %(message)s")


os.environ.setdefault("DJANGO_SETTINGS_MODULE", "ui.settings")
import django
django.setup()
