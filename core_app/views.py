from http.client import HTTPResponse

from django.http import HttpRequest, HttpResponse
from django.http.response import Http404
from django.views import generic
from django.shortcuts import render

from core_app.models import (
    ShowTheme,
    ShowSession,
    Ticket,
    Reservation,
    PlanetariumDome,
    AstronomyShow,
)


def index(request: HttpRequest) -> HttpResponse:
    context = {}

    if request.user.is_authenticated:
        context["username"] = request.user.username

    return render(request, "index.html", context)


def show_themes_list_view(request: HttpRequest) -> HttpResponse:
    show_themes = ShowTheme.objects.all()

    context = {"show_themes": show_themes}

    return render(request, "show_themes/show_themes_list.html", context)

def show_themes_detail(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        show_theme = ShowTheme.objects.get(pk=pk)
    except ShowTheme.DoesNotExist:
        raise Http404("Show Theme does not exist")

    context = {
        "show_theme": show_theme
    }
    return render(request, "show_themes/show_themes_detail.html", context)

class ShowSessionsListView(generic.ListView):
    model = ShowSession
    queryset = ShowSession.objects.select_related("astronomy_show", "planetarium_dome")
    context_object_name = "show_sessions"
    template_name = "show_sessions/show_sessions_list.html"


class ShowSessionsDetailView(generic.DetailView):
    model = ShowSession
    queryset = ShowSession.objects.select_related("astronomy_show", "planetarium_dome")
    context_object_name = "show_session"
    template_name = "show_sessions/show_session_detail.html"

class TicketListView(generic.ListView):
    model = Ticket
    queryset = Ticket.objects.select_related("show_sessions", "reserve").select_related("show_sessions__astronomy_show", "show_sessions__planetarium_dome")
    context_object_name = "tickets"
    template_name = "tickets/ticket_list.html"


class ReservationListView(generic.ListView):
    model = Reservation
    context_object_name = "reservations"
    template_name = "reservations/reservations_list.html"


class PlanetariumDomeListView(generic.ListView):
    model = PlanetariumDome
    context_object_name = "planetarium_domes"
    template_name = "planetarium_domes/planetarium_domes_list.html"


class AstronomyShowListView(generic.ListView):
    model = AstronomyShow
    context_object_name = "astronomy_shows"
    template_name = "astronomy_shows/astronomy_shows_list.html"
