from django.db import connection
import PostgreSQL

from FoodDB import singleton


@singleton
class DB(PostgreSQL.DB):
    def __init__(self):
        self.db = connection
