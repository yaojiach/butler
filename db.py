import sqlite3
import csv

DB = 'db.sqlite3'
TBL = 'machine_state'

class LiteDB(object):
    def __init__(self):
        self.conn = sqlite3.connect('db.sqlite3')
    def __del__(self):
        self.conn.close()
    def create(self):
        c = self.conn.cursor()
        c.execute('''
                  CREATE TABLE {tn} (uid INTEGER PRIMARY KEY, 
                  load_timestamp TEXT,
                  load_state TEXT)
                  '''.format(tn='machine_state'))
        self.conn.commit()
    def teardown(self):
        c = self.conn.cursor()
        c.execute('DROP TABLE IF EXISTS machine_state')
        self.conn.commit()
    def to_csv(self, tbl):
        c = self.conn.cursor()
        d = c.execute('SELECT * FROM {tn}'.format(tn=TBL))
        with open('data.csv', 'w') as f:
            wr = csv.writer(f)
            wr.writerow(['id', 'timestamp', 'state'])
            wr.writerows(d)
    def post(self, ts, st):
        c = self.conn.cursor()
        c.execute('''
                  INSERT INTO {tn} 
                  (load_timestamp, load_state) VALUES (\'{ts}\', \'{st}\')
                  '''.format(tn='machine_state', ts=ts, st=st))
        self.conn.commit()
    def get_one(self):
        c = self.conn.cursor()
        c.execute('''
                  SELECT *  FROM {tn} 
                  ORDER BY uid DESC LIMIT 1
                  '''.format(tn=TBL))
        r = c.fetchone()
        return {'ts': r[1], 'st': r[2]}
if __name__ == '__main__':
    import argparse
    ap = argparse.ArgumentParser(description='DB')
    ap.add_argument('--init', action='store_true')
    ap.add_argument('--report', action='store_true')
    args = ap.parse_args()
    init = args.init
    report = args.report
    if init:
        ldb = LiteDB()
        ldb.teardown()
        ldb.create()
        ldb.post(ts='2012-01-01', st='test')
        del ldb
    if report:
        ldb = LiteDB()
        ldb.to_csv(tbl=TBL)
        del ldb

