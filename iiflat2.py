import os
import uuid
from time import time
from glob import glob
from whoosh.fields import SchemaClass, FieldType, ID, STORED, FieldConfigurationError
from whoosh.index import create_in, open_dir, FileIndex
from whoosh.qparser import QueryParser
from jsondata import load_jsondata
from iiflat import ii_flat, ii_filter

class DocRaw(SchemaClass):
    '''

    '''

    ii_id = ID(stored=True, unique=True)
    ii_data = STORED()


class DocCollection:
    '''

    '''

    def __init__(self, indexer: FileIndex) -> None:
        self.indexer = indexer

    def optimize(self):
        with self.indexer.writer() as w:
            w.optimize = True

    def search(self, text, field='name', pagenum=1, pagelen=30):
        lt = time()
        with self.indexer.searcher() as s:
            qt = time()
            p = QueryParser(f'{field}_index', self.indexer.schema)
            q = p.parse(text)
            st = time()
            rows = s.search_page(q, pagenum, pagelen=pagelen)
            et = time()
            rs = [r.get('data') for r in rows]
            ot = time()
            print(f'l: {qt - lt:.6f}s | q: {st - qt:.6f}s | s: {et - st:.6f}s | o: {ot - et:.6f}s')
            return rs

    def _new_doc(self, data):
        d = ii_flat(data)
        r = {
            'ii_id': uuid.uuid1().hex,
            'ii_data': data,
        }
        rt = {}
        for k, v in d.items():
            vt, vd = ii_filter(v)
            if vd is None:
                continue
            if k in self.indexer.schema:
                nt = type(self.indexer.schema[k])
                if isinstance(vt, nt):
                    r[k] = vd
                else:
                    print(f'invalid field type {k} {nt} => {vt} | {vd}')
            elif vt is not None:
                r[k] = vd
                if isinstance(vt, FieldType):
                    rt[k] = vt
                else:
                    print(f'not FieldType {k} {vt}')
        return r, rt

    def _new_field(self, f):
        with self.indexer.writer() as w:
            w.optimize = True
            for k, vt in f.items():
                try:
                    w.add_field(k, vt)
                except FieldConfigurationError as e:
                    print(f'FieldConfigurationError: {k} => {vt} => {e}')

    def add_doc(self, data, **argkw):
        '''
        添加单文档。
        '''

        d, f = self._new_doc(data)
        self._new_field(f)
        with self.indexer.writer() as w:
            for k, v in argkw.items():
                setattr(w, k, v)
            w.add_document(**d)

    def add_docs(self, rows, **argkw):
        '''
        批量添加文档。
        '''

        rs = []
        rt = {}
        for row in rows:
            d, t = self._new_doc(row)
            rs.append(d)
            rt.update(t)
        for k, v in rt.items():
            print(f'{k} => {v}')
        self._new_field(rt)
        with self.indexer.writer() as w:
            for k, v in argkw.items():
                setattr(w, k, v)
            for row in rs:
                w.add_document(**d)


def open_collection(name: str) -> DocCollection:
    '''
    打开文档集，没有则创建。
    '''
    
    p = f'rt/{name}'
    if not os.path.isdir(p):
        os.makedirs(p)
        i = create_in(p, DocRaw())
        return DocCollection(i)
    i = open_dir(p)
    return DocCollection(i)


def test():
    dc = open_collection('iiflatt')
    for p in glob('rtd/*/*.json'):
        print(f'load {p}')
        r = load_jsondata(p)
        dc.add_docs(r)
    


if '__main__' == __name__:
    test()
