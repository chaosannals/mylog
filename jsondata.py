from datetime import datetime
import os
import json
import pymysql
from conf.jsondata_cnf import *


def slz_data(row):
    for rk, rv in row.items():
        if isinstance(rv, datetime):
            row[rk] = f'dt:{rv.strftime("%Y-%m-%d %H:%M:%S")}'
        elif isinstance(rv, str):
            row[rk] = f's:{rv}'
        elif isinstance(rv, int):
            row[rk] = f'i:{rv}'
        elif isinstance(rv, bytes):
            ht = ''.join([f'{b:02X}' for b in rv])
            row[rk] = f'b:{ht}'
    return row


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
        last = dbkit_find(db, f'SELECT MAX({k}) AS mid FROM {t}')
        mid = last['mid']
        for sid in range(0, mid, step):
            eid = sid + step
            rows = dbkit_search(
                db, f'SELECT * FROM {t} WHERE {k} >= {sid} AND {k} < {eid}')
            # 转换
            for row in rows:
                row = slz_data(row)
            # 写文件
            fn = f'{dirname}/{sid}-{eid}.json'
            with open(fn, 'w', encoding='utf8') as w:
                w.write(json.dumps(rows, ensure_ascii=False))


if '__main__' == __name__:
    main()
