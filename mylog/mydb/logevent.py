from peewee import *

class LogEvent(Model):
    class Meta:
        table_name='ml_log_event'

    position = IntegerField(unique=True)