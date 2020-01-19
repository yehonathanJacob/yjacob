from django.conf import settings
import pytest


@pytest.fixture(scope='session')
def django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'food',
        'USER': 'food',
        'PASSWORD': 'foooddd',
        'HOST': 'pgsql',
        'PORT': '5432',
    }


@pytest.fixture(scope='session')
def base_url():
    return 'http://localhost:8000/food/'
