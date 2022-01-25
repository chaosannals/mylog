import os
from peewee import *
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser

tester = Schema(
    testname=ID(stored=True),
    description=TEXT(stored=True),
    tags=KEYWORD
)

ixt_dir = 'rt/tester'
if not os.path.isdir(ixt_dir):
    os.makedirs(ixt_dir)
    ixt = create_in(ixt_dir, tester)
else:
    ixt = open_dir(ixt_dir)

rt = ixt.reader()

wt = ixt.writer()
wt.add_document(
    testname='aaaaa222',
    description='aaaaa content',
    tags=['aaa', 'bbb', ] # 官方示例是 空格或逗号 隔开的字符串。
)
wt.commit()

with ixt.searcher() as searcher:
    query = QueryParser(
        'description',
        ixt.schema
    ).parse('content')
    rs = searcher.search(query)
    print([r for r in rs])

    q2 = QueryParser(
        'tags',
        ixt.schema
    ).parse('aaa')
    rs2 = searcher.search(q2)
    print([r for r in rs2])


####################
class TestJobSchema(SchemaClass):
    idtest = ID(stored=True)
    texttest = TEXT(stored=True, analyzer=StemmingAnalyzer)
    tags = KEYWORD

ixtj_dir = 'rt/testjob'
if not os.path.isdir(ixtj_dir):
    os.makedirs(ixtj_dir)
ixtj = create_in(ixtj_dir, TestJobSchema())