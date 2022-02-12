import os
import json
import uuid
from glob import glob
from whoosh.fields import SchemaClass, FieldType, ID, STORED, TEXT, KEYWORD
from whoosh.index import create_in, open_dir, FileIndex
from jsondata import load_jsondata


class DocRaw(SchemaClass):
    '''

    '''

    id = ID(stored=True, unique=True)
    data = STORED()


class DocCollection:
    '''

    '''

    def __init__(self, indexer: FileIndex) -> None:
        self.indexer = indexer

    def add_index(self, f: str, ft: FieldType):
        with self.indexer.writer() as w:
            w.optimize = True
            w.add_field(f, ft)
        

    def del_index(self, f: str):
        with self.indexer.writer() as w:
            w.optimize = True
            w.remove_field(f)

    @staticmethod
    def _new_doc(data):
        return {
            'id': uuid.uuid1().hex,
            'data': json.dumps(data, ensure_ascii=False),
        }

    def add_doc(self, data, **argkw):
        d = self._new_doc(data)
        with self.indexer.writer() as w:
            for k, v in argkw.items():
                setattr(w, k, v)
            for k, v in self.indexer.schema.items():
                if k.endswith('_index'):
                    ik = k[:-6]
                    if ik in data:
                        d[k] = data[ik]
            w.add_document(**d)

    def add_docs(self, rows, **argkw):
        fs = self.indexer.schema.items()
        with self.indexer.writer() as w:
            for k, v in argkw.items():
                setattr(w, k, v)
            for row in rows:
                d = self._new_doc(row)
                for k, v in fs:
                    if k.endswith('_index'):
                        ik = k[:-6]
                        if ik in row:
                            d[k] = row[ik]
                w.add_document(**d)


def open_collection(name: str) -> DocCollection:
    p = f'rt/{name}'
    if not os.path.isdir(p):
        os.makedirs(p)
        i = create_in(p, DocRaw())
        return DocCollection(i)
    i = open_dir(p)
    return DocCollection(i)


def test():
    dc = open_collection('iikitt')
    dc.add_index('key', TEXT())
    dc.del_index('key')
    for p in glob('rtd/*/*.json'):
        print(f'load {p}')
        r = load_jsondata(p)
        dc.add_docs(r)
    


if '__main__' == __name__:
    test()
