import os
import jieba
from glob import glob
from pymongo import MongoClient
from jsondata import load2_jsondata

client = MongoClient()


def main():
    for p in glob('rtd/*/*.json'):
        dn = os.path.dirname(p)
        d = os.path.basename(dn)
        print(f'load {d} {p}')
        ds = getattr(client.test, d)
        rs = load2_jsondata(p)
        if len(rs) > 0:
            for r in rs:
                if r['name'] is not None:
                    words = jieba.cut_for_search(r['name'])
                    r['words'] = ' '.join(words)
            ds.insert_many(rs)
        
        

if __name__ == '__main__':
    main()