import json
from glob import glob
from whoosh.fields import KEYWORD

def load_json(p):
    with open(p, 'r', encoding='utf8') as reader:
        t = reader.read()
        return json.loads(t)

def make_schema(d: dict):
    r = []
    for k,v in d.items():
        if isinstance(v, str):
            r.append((k, 'string'))
        elif isinstance(v, list):
            r.append((k, KEYWORD(stored=True, sortable=True)))
        elif isinstance(v, int):
            r.append((k, 'int'))
        elif isinstance(v, dict):
            cr = make_schema(v)
            for crr in cr:
                r.append((f'{k}.{crr[0]}', crr[1]))
    return r

def main():
    '''
    
    '''
    ps = glob('asset/data.*.json')
    for p in ps:
        d = load_json(p)
        print('==================')
        for s in make_schema(d):
            print(s)

if '__main__' == __name__:
    main()