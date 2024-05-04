from django.urls import path

from .views import *


urlpatterns = [
    path('', Temp.as_view()),
]