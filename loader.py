from pymysqlreplication import BinLogStreamReader
from conf.bl_cnf import *

BINLOG_HEAD=b'\xFEbin'

stream = BinLogStreamReader(
    connection_settings=mysql_settings,
    log_file=log_file,
    log_pos=log_pos,
    server_id=100
)

count = 4
for b in stream:
    # d = b.packet.packet._data
    # count += len(d)
    # print(d)
    b.dump()
    print(b.packet.log_pos)

print(f'c: {count}')
stream.close()
