import os
import json
import uuid
from whoosh.fields import SchemaClass, FieldType, ID, STORED, TEXT, KEYWORD
from whoosh.index import create_in, open_dir, FileIndex


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


def new_collection(name: str) -> DocCollection:
    p = f'rt/{name}'
    if not os.path.isdir(p):
        os.makedirs(p)
        i = create_in(p, DocRaw())
        return DocCollection(i)
    i = open_dir(p)
    return DocCollection(i)


def new_doc(data):
    return {
        'id': uuid.uuid1(),
        'data': json.dumps(data, ensure_ascii=False),
    }


def test():
    dc = new_collection('iikitt')
    dc.add_index('key', TEXT())
    dc.del_index('key')


if '__main__' == __name__:
    test()
