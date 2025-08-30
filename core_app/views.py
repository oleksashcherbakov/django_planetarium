from http.client import HTTPResponse

from django.http import HttpRequest, HttpResponse
from django.shortcuts import render


def index(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        username = request.user.username
        return HttpResponse(f"<p>Hello {username}!!! </p>")
    return HttpResponse("<p>Hello Anonymous!!!</p>")
