import os
import json
from time import time_ns
from peewee import *
from whoosh.index import create_in, open_dir
from whoosh.fields import *
from whoosh.analysis import StemmingAnalyzer
from whoosh.qparser import QueryParser
from zha import zh_analyzer

# stored=False 只有索引，查询结果没有该值。
tester = Schema(
    testname=ID(unique=True, stored=False),
    description=TEXT(stored=False, analyzer=zh_analyzer()),
    tags=KEYWORD(stored=False),
    all=STORED()
)

ixt_dir = 'rt/tester'
if not os.path.isdir(ixt_dir):
    os.makedirs(ixt_dir)
    ixt = create_in(ixt_dir, tester)
else:
    ixt = open_dir(ixt_dir)

# rt = ixt.reader()

wt = ixt.writer()
# 即使 ID unique=True 相同ID还是会多添加文档，而且 ID 只索引最后一个。
with wt.group():
    s = time_ns()
    for i in range(10):
        ai = {
            'testname':f'G文档{s + i}',
            'description':f'G文档描述 {s} {i}',
            'tags':'aaa bbb',
        }
        wt.add_document(all=json.dumps(ai, ensure_ascii=False), **ai)
d1 = {
    'testname':'aaaaa222',
    'description':'中文描述分词content',
    'tags': ['aaa', 'bbb', ] # 官方示例是 空格或逗号 隔开的字符串。列表是多添加的，默认取了第一个。
}
wt.add_document(all=json.dumps(d1, ensure_ascii=False), **d1)

u1 = {
    'testname':'aaaaa222',
    'description':'更新后32中文描述分词content',
    'tags':'bbb ccc'
}
wt.update_document(all=json.dumps(u1, ensure_ascii=False),**u1)

# 使用 更新时没有会添加，所以使用 update_document 添加文档更符合常规。
# 但是会更慢，在自动生成唯一ID 的场景不适用。
u2 = {
    'testname':'aaaaa3333',
    'description':'更新后33333333中文描述分词content',
    'tags':'bbb ccc'
}
wt.update_document(all=json.dumps(u2, ensure_ascii=False),**u2)
wt.commit()

with ixt.searcher() as searcher:
    query = QueryParser(
        'description',
        ixt.schema
    ).parse('中文')
    rs = searcher.search(query)
    r1 = [r for r in rs]
    print(f'长度： {len(r1)}')
    for r1r in r1:
        print(r1r.docnum, r1r)

    q2 = QueryParser(
        'tags',
        ixt.schema
    ).parse('bbb')
    rs2 = searcher.search(q2)
    r2 = [r for r in rs2]
    print(f'长度： {len(r2)}')
    for r2r in r2:
        print(r2r.docnum, r2r)


####################
class TestJobSchema(SchemaClass):
    idtest = ID(unique=True, stored=True)
    texttest = TEXT(stored=True, analyzer=StemmingAnalyzer)
    tags = KEYWORD

ixtj_dir = 'rt/testjob'
if not os.path.isdir(ixtj_dir):
    os.makedirs(ixtj_dir)
ixtj = create_in(ixtj_dir, TestJobSchema())