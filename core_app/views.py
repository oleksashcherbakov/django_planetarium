from http.client import HTTPResponse

from django.http import HttpRequest, HttpResponse
from django.views import generic
from django.shortcuts import render

from core_app.models import ShowTheme, ShowSession, Ticket, Reservation, PlanetariumDome, AstronomyShow


def index(request: HttpRequest) -> HttpResponse:
    context = {}

    if request.user.is_authenticated:
        context["username"] = request.user.username

    return render(request, "index.html", context)




def show_themes_list(request: HttpRequest) -> HttpResponse:
    show_themes = ShowTheme.objects.all()

    context = {"show_themes": show_themes}

    return render(request, "show_themes/show_themes_list.html", context)


class ShowSessionsListView(generic.ListView):
    model = ShowSession
    context_object_name = "show_sessions"
    template_name = "show_sessions/show_sessions_list.html"


class TicketListView(generic.ListView):
    model = Ticket
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
