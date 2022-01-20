from pymysqlreplication import BinLogStreamReader

BINLOG_HEAD=b'\xFEbin'

mysql_settings = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'exert',
    'passwd': 'password'
}

stream = BinLogStreamReader(
    connection_settings=mysql_settings,
    # log_file='binlog.000260',
    # log_pos=4,
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
