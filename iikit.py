import json
import uuid
from whoosh.fields import SchemaClass, ID, STORED

class DocRaw(SchemaClass):
    '''
    
    '''

    _id = ID(stored=True)
    _data = STORED()

def new_doc(data):
    return {
        '_id': uuid.uuid1(),
        '_data': json.dumps(data, ensure_ascii=False),
    }
