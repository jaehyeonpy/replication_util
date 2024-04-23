import datetime

from django.db import models


# I could not find the exact maximum byte size of a sql statement of ANNOTATE_ROWS_EVENT, QUERY EVENT:
# mariadb can receive and save a sql statement whose length is unlimited through multiple packets,
# pymysql, python-mysql-replication send the sql statement the same way.
#
# so, I set the value based on this: 
# pymysql, python-mysql-replication usually sends a sql statement in a packet, less than the max size a packet can have.
SQL_STATEMENT_MAX_LENGTH = 2**32 - 1 - 19

# python-mysql-replication binlogevent.__name__'s max length is less than 30.
EVENT_TYPE_MAX_LENGTH = 30

# pymysql, python-mysql-replication does not specify the length of database name,
# mariadb official document says the name is in 64 bytes,
# also the name is usually in english, so,
DB_NAME_MAX_LENGTH = 64


class MariadbAnnotateRowsEventModelManager(models.Manager):
    def create_model(self, id, binlogevent):
        self.create(
            id=id,
            time=datetime.datetime.fromtimestamp(binlogevent.timestamp),
            sql_statement=binlogevent.sql_statement
        )

class QueryEventModelManager(models.Manager):
    def create_model(self, id, binlogevent):
        self.create(
            id=id,
            time=datetime.datetime.fromtimestamp(binlogevent.timestamp),
            type=type(binlogevent).__name__,
            db_name=binlogevent.schema,
            exec_time=binlogevent.execution_time,
            sql_statement=binlogevent.query
        )


class MariadbAnnotateRowsEventModel(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    time = models.DateTimeField()
    sql_statement = models.CharField(max_length=SQL_STATEMENT_MAX_LENGTH)

    objects = MariadbAnnotateRowsEventModelManager()

    def __str__(self):
        return f"""
            id: {self.id}, 
            time: {self.time},
            sql_statement: {self.sql_statement}
        """

class QueryEventModel(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    time = models.DateTimeField()
    type = models.CharField(max_length=EVENT_TYPE_MAX_LENGTH) 
    db_name = models.CharField(max_length=DB_NAME_MAX_LENGTH) 
    exec_time = models.PositiveIntegerField()
    sql_statement = models.CharField(max_length=SQL_STATEMENT_MAX_LENGTH)

    objects = QueryEventModelManager()

    def __str__(self):
        return f"""
            id: {self.id}, 
            time: {self.time},
            type: {self.type},
            db_name: {self.db_name},
            exec_time: {self.exec_time},
            sql_statement: {self.sql_statement}
        """
