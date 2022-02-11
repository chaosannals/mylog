import os
from time import time_ns
from peewee import *
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser
from zha import zh_analyzer

ixt_dir = 'rt/tester'
ixt = open_dir(ixt_dir)
wt = ixt.writer()
wt.remove_field('tags')
wt.commit()

with ixt.searcher() as searcher:
    query = QueryParser(
        'description',
        ixt.schema
    ).parse('中文')
    rs = searcher.search(query)
    r1 = [r for r in rs]
    print(f'长度： {len(r1)} \r\n {r1}')

    q2 = QueryParser(
        'tags',
        ixt.schema
    ).parse('bbb')
    rs2 = searcher.search(q2)
    r2 = [r for r in rs2]
    print(f'长度： {len(r2)} \r\n {r2}')


####################
class TestJobSchema(SchemaClass):
    idtest = ID(unique=True, stored=True)
    texttest = TEXT(stored=True, analyzer=StemmingAnalyzer)
    tags = KEYWORD

ixtj_dir = 'rt/testjob'
if not os.path.isdir(ixtj_dir):
    os.makedirs(ixtj_dir)
ixtj = create_in(ixtj_dir, TestJobSchema())