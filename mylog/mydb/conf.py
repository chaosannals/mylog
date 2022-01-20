from peewee import *

class DbConf(Model):
    class Meta:
        table_name = 'ml_dbconf'

    host = CharField(160)
    port = IntegerField()
    user = CharField(16)
    password = CharField(50)