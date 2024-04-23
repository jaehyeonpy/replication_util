from pymysqlreplication import BinLogStreamReader
from pymysqlreplication.event import *

from django.http import JsonResponse

from .models import *


MYSQL_SETTINGS = {"host": "127.0.0.1", "port": 3306, "user": "root", "passwd": "1234"}

ONLY_EVENTS = [
        QueryEvent,
        MariadbAnnotateRowsEvent
    ]

event_to_model = {
        'QueryEvent': QueryEventModel,
        'MariadbAnnotateRowsEvent': MariadbAnnotateRowsEventModel
    }


def temp(request):
    binlog_stream = BinLogStreamReader(
        connection_settings=MYSQL_SETTINGS, server_id=3, 
        blocking=True, only_events=ONLY_EVENTS,
        is_mariadb=True, annotate_rows_event=True
    )

    for binlogevent in binlog_stream:
        event_model = event_to_model[type(binlogevent).__name__]

        model_next_row_num = event_model.objects.count() + 1
        event_model.objects.create_model(model_next_row_num, binlogevent)
        print(event_model.__name__, model_next_row_num)

    return JsonResponse({})