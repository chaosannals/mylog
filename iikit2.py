from whoosh.fields import TEXT
from iikit import open_collection
from zha import zh_analyzer

def test():
    dc = open_collection('iikitt')
    # dc.add_index('name', TEXT(stored=False, analyzer=zh_analyzer()))
    dc.optimize()


if '__main__' == __name__:
    test()
