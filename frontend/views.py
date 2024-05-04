import threading

from django.http import JsonResponse
from django.views import View

from .replication import recv_log
from replication_util.settings import IS_LOG_RECV_THREAD_ENABLED, LOG_RECV_THREAD


class Temp(View):
    def get(self, request):
        # Django recommends doing async things for this kind of work, but,
        # I did it by using thread temporarily.
        #
        # I know using global variable is one of bad practices, but,
        # it is okay because the variables are used in the following limited way.
        #
        # Django usually put variables for state management in settings.py, so,
        # I import and use necessary ones from there.
        global IS_LOG_RECV_THREAD_ENABLED
        global LOG_RECV_THREAD

        if IS_LOG_RECV_THREAD_ENABLED == False:
            IS_LOG_RECV_THREAD_ENABLED = True
            LOG_RECV_THREAD = threading.Thread(target=recv_log)
            LOG_RECV_THREAD.start()

        return JsonResponse({})