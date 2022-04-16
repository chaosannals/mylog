import os
from glob import glob
from typejson.serialization import TypeJsonSerializer
from jsondata import load_jsondata


tjs = TypeJsonSerializer()
for p in glob('rtd/*/*.json'):
    dn = os.path.dirname(p)
    d = os.path.basename(dn)
    n = os.path.basename(p)

    td = f'tjd/{d}'
    if not os.path.isdir(td):
        os.makedirs(td)

    print(f'load {d} {n}')
    rs = load_jsondata(p)
    with open(f'{td}/{n}', 'w', encoding='utf8') as fp:
        tjs.dump(rs, fp)