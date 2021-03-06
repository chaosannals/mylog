from datetime import date, datetime
from decimal import Decimal
from whoosh.fields import TEXT, KEYWORD, NUMERIC, DATETIME, BOOLEAN
from zha import zh_analyzer

def ii_flat(data: dict) -> dict:
    '''
    
    '''

    r = {}
    for k, v in data.items():
        if isinstance(v, dict):
            for k1, v1 in ii_flat(v).items():
                kk = f'{k}.{k1}'
                if kk in r:
                    if isinstance(r[kk], list):
                        r[kk].append(v1)
                    else:
                        r[kk] = [r[kk], v1]
                else:
                    r[kk] = v1
        elif isinstance(v, list):
            vr = []
            for vi in v:
                if isinstance(vi, dict):
                    for k1, v1 in ii_flat(vi).items():
                        kk = f'{k}[{k1}]'
                        if kk in r:
                            if isinstance(r[kk], list):
                                r[kk].append(v1)
                            else:
                                r[kk] = [r[kk], v1]
                        else:
                            r[kk] = v1
                elif isinstance(vi, list):
                    vr.append(vi) # 多维向量不为索引
                else:
                    vr.append(vi)
            if k in r:
                if isinstance(r[k], list):
                    r[k].append(vr)
                else:
                    r[k] = [r[k], vr]
            else:
                r[k] = vr
        else:
            if k in r:
                if isinstance(r[k], list):
                    r[k].append(v)
                else:
                    r[k] = [r[k], v]
            else:
                r[k] = v

    return r

def ii_filter(v):
    if isinstance(v, list):
        for i in v:
            if isinstance(i, list):
                return None, v
        return KEYWORD(stored=False) if len(v) > 0 else None, v
    if isinstance(v, int):
        return NUMERIC(stored=False, numtype=int, bits=64), v
    if isinstance(v, float):
        return NUMERIC(stored=False, numtype=float, bits=64), v
    if isinstance(v, Decimal):
        return NUMERIC(stored=False, decimal_places=3), v
    if isinstance(v, datetime) or isinstance(v, date):
        return DATETIME(stored=False), v
    if isinstance(v, bool):
        return BOOLEAN(stored=False), v
    if isinstance(v, str):
        return TEXT(analyzer=zh_analyzer(), stored=False), v
    return None, v


def test():
    '''
    '''
    a = {
        'ak': 123,
        'bk': [1,2,3],
        'ck': [
            {
                'ck1ak': 1,
            },
            {
                'ck1ak': 123,
                'ck2bk': [ 1,2,3 ],
                'ck2ck': [
                    {
                        'ck2ak': 123,
                    },
                    123,
                    '1234',
                ],
            },
            [
                123, 456, [ 234, '455', [234, 434,343, [4343434, 343,'34343']]]
            ],
            [
                {
                    'ck4_1ak': 123,
                },
                {
                    'ck4_2ak': [1, 2, 3]
                },
            ],
        ],
        'dk': [
            {
                'dkak': 1,
                'dkbk': 'a',
            },
            {
                'dkak': 2,
                'dkbk': 'b',
            },
            {
                'dkak': 3,
                'dkbk': 'c',
            },
            {
                'dkak': 3,
                'dkbk': ['d', 'c'],
            },
            {
                'dkak': 3,
                'dkbk': {
                    'd': 1,
                    'c': 2,
                },
            },
            {
                'dkak': 3,
                'dkbk': {
                    'd': 3,
                    'c': 4,
                },
            },
        ]
    }
    rs = ii_flat(a)
    for k, v in rs.items():
        print(k, ' => ', ii_filter(v))

if '__main__' == __name__:
    test()