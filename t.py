import uuid

u = uuid.uuid1()
print(u.hex)

a = 's:aaa:ddd:ccc'.split(':', 1)
print(f"{a[0] == 'd'}")

b = 'bbb_index'
if b.endswith('_index'):
    bn = b[:-6]
    print(bn)