import pickle
from decimal import Decimal
import uuid

u = uuid.uuid1()
print(u.hex)

a = 's:aaa:ddd:ccc'.split(':', 1)
print(f"{a[0] == 'd'}")

b = 'bbb_index'
if b.endswith('_index'):
    bn = b[:-6]
    print(bn)

p = pickle.dumps({
    'ddd': Decimal(100)
})

print(p)


kd = {
    'aaa_index': 123,
    'bbb_index': 123,
    'cc': '123',
    'ddd': 123,
}

for k, ki in [(k, k[:-6]) for k in filter(lambda i: i.endswith('_index'), kd.keys())]:
    print(k)