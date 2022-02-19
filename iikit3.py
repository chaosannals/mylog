
from time import time
from whoosh.fields import TEXT
from whoosh.qparser import QueryParser
from iikit import open_collection
from zha import zh_analyzer

def test():
    dc = open_collection('iikitt')
    dc.search('积木', limit=1000)
    dc.search('泡泡', limit=1000)
    dc.search('风车', limit=1000)
    


if '__main__' == __name__:
    test()
