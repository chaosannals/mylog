
from whoosh.fields import TEXT
from whoosh.qparser import QueryParser
from iikit import open_collection
from zha import zh_analyzer

def test():
    dc = open_collection('iikitt')
    with dc.indexer.searcher() as s:
        q = QueryParser('name_index', '积木')
        rows = s.search(q)
        for r in rows:
            print(r)
    


if '__main__' == __name__:
    test()
