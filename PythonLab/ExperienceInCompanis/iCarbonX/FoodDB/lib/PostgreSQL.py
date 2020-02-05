import logging,sys
import psycopg2 as dbapi2
from datetime import datetime
from collections import defaultdict

def dt(timestamp):
    return datetime.fromtimestamp(int(timestamp))    


class DB(object):
    host=None
    user=None
    password=None
    dbname=None

    def __init__(self, host=None, user=None, password=None, dbname=None):
        if host:
            self.host = host
        if user:
            self.user = user
        if password:
            self.password = password
        if dbname:
            self.dbname = dbname
        #print('Connecting to %s %s %s %s', self.host,self.user,self.password,self.dbname)
        self.connect()

    def connect(self):
        logging.info('Connecting to %s %s %s %s', self.host,self.user,self.password,self.dbname)
        self.db = dbapi2.connect(host=self.host, user=self.user, password=self.password, dbname=self.dbname)
        self.db.autocommit = True
        status = self.check_connection()
        logging.info('Connection status %s' , "ok" if status else "fail")
        return status

    def check_connection(self):
        try :
            v = self.select_as_value("select 1 as dummy")
            if v != 1:
                logging.info('check_connection failed v=%d', v)
                return False
            else:
                return True
        except :
            return False


    def check_reconnect(self):
        if self.check_connection():
            return 
        self.connect()
        if self.check_connection():
            return 
        raise Exception("Database connetion kaput")
    
    def execute(self, sql, params=None):
        try:
            cur  = self.db.cursor()
            cur.execute(sql,params)
            return cur
        except Exception as e:
            if not self.check_connection():
                self.connect()
                cur  = self.db.cursor()
                cur.execute(sql,params)
                return cur
            else:
                raise e

    def insert(self, sql,params=None):
        cur  = self.db.cursor()
        #cur.execute(sql,params)        
        cur =  self.execute(sql,params)
        return self.select_as_value('select lastval()')


    def select_as_value(self, sql,params=None):
        cur =  self.execute(sql,params)
        for x in cur :
            return x[0]

    def select_as_row(self, sql,params=None):
        cur =  self.execute(sql,params)
        for x in cur :
            return x


    def select_as_column(self, sql,params=None):
        cur =  self.execute(sql,params)
        return [x[0] for x in cur]

    def select_as_set(self, sql,params=None):
        cur =  self.execute(sql,params)
        return set([x[0] for x in cur])

    def select_as_table(self, sql,params=None):
        cur =  self.execute(sql,params)
        return [x for x in cur]

    def select_row_as_dict(self, sql,params=None):
        cur =  self.execute(sql,params)
        names = [x[0] for x in cur.description]
        for x in cur:
            return dict(zip(names,x))

    def select_as_dict_list(self, sql,params=None):
        cur =  self.execute(sql,params)
        names = [x[0] for x in cur.description]
        return [dict(zip(names,x)) for x in cur]

    def select_as_dict(self, sql,params=None, result_dict=None):
        cur =  self.execute(sql,params)
        #return dict([(x[0],x[1]) for x in cur])

        _dict = {} if result_dict is None else result_dict
        for x in cur:
            _dict[x[0]]=x[1]
        return _dict

    def select_as_dict_dict(self, sql,params=None, result_dict=None):
        cur =  self.execute(sql,params)
        names = [x[0] for x in cur.description]
        _dict = {} if result_dict is None else result_dict
        _dict.update({x[0]: dict(zip(names,x)) for x in cur})
        return _dict

    def select_as_dict_dict2(self, sql,params=None):
        cur =  self.execute(sql,params)
        res = {} #defaultdict(lambda: {})
        for x in cur:            
            if x[0] not in res:
                res[x[0]] = {}
            res[x[0]][x[1]] = x[2]
        return res

    def select_lambda(self, sql,f,params=None):
        cur =  self.execute(sql,params)
        return [f(x) for x in cur]

    def save_sql(self, sql,params=None, OUT=sys.stdout, FS="\t", RS="\n"):
        cur =  self.execute(sql,params)
        for x in cur:            
            OUT.write(FS.join(map(str,x)).encode("utf-8"))
            OUT.write(RS)



