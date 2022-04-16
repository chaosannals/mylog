from datetime import datetime, date
from decimal import Decimal
from bson import Decimal128
import os
import json
import pymysql
from conf.jsondata_cnf import *


def slz_data(row: dict):
    for rk, rv in row.items():
        if isinstance(rv, datetime):
            row[rk] = f'dt:{rv.strftime("%Y-%m-%d %H:%M:%S")}'
        elif isinstance(rv, date):
            row[rk] = f'd:{rv.strftime("%Y-%m-%d")}'
        elif isinstance(rv, str):
            row[rk] = f's:{rv}'
        elif isinstance(rv, int):
            row[rk] = f'i:{rv}'
        elif isinstance(rv, float):
            row[rk] = f'f:{rv}'
        elif isinstance(rv, Decimal):
            row[rk] = f'n:{rv}'
        elif isinstance(rv, bytes):
            row[rk] = f'b:{rv.hex()}'
    return row

def uns_data(row: dict):
    for rk, rv in row.items():
        if rv is None:
            continue
        tv = rv.split(':', 1)
        t = tv[0]
        v = tv[1]
        if t == 'dt':
            row[rk] = datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
        elif t == 'd':
            row[rk] = datetime.strptime(v, '%Y-%m-%d').date()
        elif t == 's':
            row[rk] = v
        elif t == 'i':
            row[rk] = int(v)
        elif t == 'f':
            row[rk] = float(v)
        elif t == 'n':
            row[rk] = Decimal(v)
        elif t == 'b':
            row[rk] = bytes.fromhex(v)
    return row

def uns2_data(row: dict):
    for rk, rv in row.items():
        if rv is None:
            continue
        tv = rv.split(':', 1)
        t = tv[0]
        v = tv[1]
        if t == 'dt':
            row[rk] = datetime.strptime(v, '%Y-%m-%d %H:%M:%S')
        elif t == 'd':
            row[rk] = date.strptime(v, '%Y-%m-%d')
        elif t == 's':
            row[rk] = v
        elif t == 'i':
            row[rk] = int(v)
        elif t == 'f':
            row[rk] = float(v)
        elif t == 'n':
            row[rk] = Decimal128(v)
        elif t == 'b':
            row[rk] = bytes.fromhex(v)
    return row

def load_jsondata(p):
    with open(p, 'r', encoding='utf8') as r:
        rows = json.loads(r.read())
        return [uns_data(row) for row in rows]

def load2_jsondata(p):
    with open(p, 'r', encoding='utf8') as r:
        rows = json.loads(r.read())
        return [uns2_data(row) for row in rows]

def dbkit_connect():
    return pymysql.connect(
        cursorclass=pymysql.cursors.DictCursor,
        **src_db_settings
    )


def dbkit_search(conn, sql, *args):
    with conn.cursor() as cursor:
        cursor.execute(sql, args)
        return cursor.fetchall()


def dbkit_find(conn, sql, *args):
    with conn.cursor() as cursor:
        cursor.execute(sql, args)
        return cursor.fetchone()


def main():
    t = data_settings['src_table']
    k = data_settings['src_key']
    step = data_settings['step']
    dirname = data_settings['dir']
    if not os.path.isdir(dirname):
        os.makedirs(dirname)
    with dbkit_connect() as db:
        start = dbkit_find(db, f'SELECT MIN({k}) AS mid FROM {t}')
        last = dbkit_find(db, f'SELECT MAX({k}) AS mid FROM {t}')
        mid = last['mid']
        mmid = start['mid']
        for sid in range(mmid, mid, step):
            eid = sid + step
            rows = dbkit_search(
                db, f'SELECT * FROM {t} WHERE {k} >= {sid} AND {k} < {eid}')
            # 转换
            rows = [slz_data(row) for row in rows]

            # 写文件
            fn = f'{dirname}/{sid}-{eid}.json'
            with open(fn, 'w', encoding='utf8') as w:
                w.write(json.dumps(rows, ensure_ascii=False))
            print(f'output: {fn}')


if '__main__' == __name__:
    main()
