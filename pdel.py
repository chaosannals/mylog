from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.event import *
from pymysqlreplication.row_event import *
from conf.bl_cnf import *

BINLOG_HEAD=b'\xFEbin'

stream = BinLogStreamReader(
    connection_settings=mysql_settings,
    log_file=log_file,
    log_pos=log_pos,
    only_schemas=only_schemas,
    only_tables=only_tables,
    only_events=[ # 只看指定事件
        RotateEvent,
        DeleteRowsEvent,
    ],
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
