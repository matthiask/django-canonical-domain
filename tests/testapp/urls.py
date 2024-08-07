from django.http import HttpResponse
from django.urls import path


urlpatterns = [
    path("", lambda request: HttpResponse("Hello world")),
    path("no-ssl", lambda request: HttpResponse("Hello world")),
]
