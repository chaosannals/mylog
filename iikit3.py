
from time import time
from whoosh.fields import TEXT
from whoosh.qparser import QueryParser
from iikit import open_collection
from zha import zh_analyzer

def test():
    dc = open_collection('iikitt')
    r1 = dc.search('积木', 'name', pagenum=30, pagelen=100)
    for r in r1:
        print(r['name'])
    r2 = dc.search('泡泡', 'name', pagenum=60, pagelen=100)
    for r in r2:
        print(r['name'])
    r3 = dc.search('风车', 'name', pagenum=100, pagelen=100)
    for r in r3:
        print(r['name'])
    


if '__main__' == __name__:
    test()
