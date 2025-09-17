from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.decorators import login_required
from django.http.response import Http404, HttpResponseRedirect
from django.views import generic
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.urls import reverse, reverse_lazy


from core_app.models import (
    ShowTheme,
    ShowSession,
    Ticket,
    Reservation,
    PlanetariumDome,
    AstronomyShow,
)


def login_view(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        return render(request, "registration/login.html")
    elif request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return HttpResponseRedirect(reverse("planetarium:index"))
        else:
            error_context = {"message": "Invalid username and/or password."}
            return render(request, "registration/login.html", context=error_context)


@login_required
def logout_view(request: HttpRequest) -> HttpResponse:
    logout(request)
    return render(request, "registration/logged_out.html")


def index(request: HttpRequest) -> HttpResponse:
    num_showtheme = ShowTheme.objects.count()
    num_showsession = ShowSession.objects.count()
    num_planetariumdome = PlanetariumDome.objects.count()
    num_astronomyshow = AstronomyShow.objects.count()

    num_visits = request.session.get("num_visits", 0) + 1
    request.session["num_visits"] = num_visits

    context = {
        "num_showtheme": num_showtheme,
        "num_showsession": num_showsession,
        "num_planetariumdome": num_planetariumdome,
        "num_astronomyshow": num_astronomyshow,
        "num_visits": num_visits,
    }

    if request.user.is_authenticated:
        context["username"] = request.user.username

    return render(request, "index.html", context)


@login_required
def show_themes_list_view(request: HttpRequest) -> HttpResponse:
    show_themes = ShowTheme.objects.all().order_by("name")
    paginator = Paginator(show_themes, 3)
    page = request.GET.get("page")

    try:
        show_themes = paginator.page(page)
    except PageNotAnInteger:
        show_themes = paginator.page(1)
    except EmptyPage:
        show_themes = paginator.page(paginator.num_pages)

    page_obj = paginator.get_page(page)
    is_paginated = page_obj.has_other_pages()

    context = {
        "show_themes": show_themes,
        "page_obj": page_obj,
        "is_paginated": is_paginated,
        "paginator": paginator,
    }

    return render(request, "show_themes/show_themes_list.html", context)


@login_required
def show_themes_detail(request: HttpRequest, pk: int) -> HttpResponse:
    try:
        show_theme = ShowTheme.objects.get(pk=pk)
    except ShowTheme.DoesNotExist:
        raise Http404("Show Theme does not exist")

    context = {"show_theme": show_theme}
    return render(request, "show_themes/show_themes_detail.html", context)


class ShowSessionsListView(LoginRequiredMixin, generic.ListView):
    model = ShowSession
    queryset = ShowSession.objects.select_related("astronomy_show", "planetarium_dome")
    context_object_name = "show_sessions"
    template_name = "show_sessions/show_sessions_list.html"
    paginate_by = 3


class ShowSessionsDetailView(LoginRequiredMixin, generic.DetailView):
    model = ShowSession
    queryset = ShowSession.objects.select_related("astronomy_show", "planetarium_dome")
    context_object_name = "show_session"
    template_name = "show_sessions/show_session_detail.html"


class ShowSessionsCreateView(LoginRequiredMixin, generic.CreateView):
    model = ShowSession
    fields = '__all__'
    template_name = "show_sessions/show_session_form.html"
    success_url = reverse_lazy("core_app:showsessions-list")


class TicketListView(LoginRequiredMixin, generic.ListView):
    model = Ticket
    queryset = Ticket.objects.select_related("show_sessions", "reserve").select_related(
        "show_sessions__astronomy_show", "show_sessions__planetarium_dome"
    )
    context_object_name = "tickets"
    template_name = "tickets/ticket_list.html"
    paginate_by = 3


class TicketDetailView(LoginRequiredMixin, generic.DetailView):
    model = Ticket
    queryset = Ticket.objects.select_related("show_sessions", "reserve").select_related(
        "show_sessions__astronomy_show", "show_sessions__planetarium_dome"
    )
    context_object_name = "ticket"
    template_name = "tickets/ticket_detail.html"


class TicketCreateView(LoginRequiredMixin, generic.CreateView):
    model = Ticket
    fields = '__all__'
    template_name = "tickets/ticket_form.html"
    success_url = reverse_lazy("core_app:tickets-list")

class ReservationListView(LoginRequiredMixin, generic.ListView):
    model = Reservation
    context_object_name = "reservations"
    template_name = "reservations/reservations_list.html"
    paginate_by = 3


class ReservationDetailView(LoginRequiredMixin, generic.DetailView):
    model = Reservation
    context_object_name = "reservation"
    template_name = "reservations/reservation_detail.html"

class ReservationCreateView(LoginRequiredMixin, generic.CreateView):
    model = Reservation
    fields = '__all__'
    template_name = "reservations/reservation_form.html"
    success_url = reverse_lazy("core_app:reservations-list")

class PlanetariumDomeListView(LoginRequiredMixin, generic.ListView):
    model = PlanetariumDome
    context_object_name = "planetarium_domes"
    template_name = "planetarium_domes/planetarium_domes_list.html"
    paginate_by = 3


class PlanetariumDomeDetailView(LoginRequiredMixin, generic.DetailView):
    model = PlanetariumDome
    queryset = PlanetariumDome.objects.prefetch_related("show_sessions")
    context_object_name = "planetarium_dome"
    template_name = "planetarium_domes/planetarium_dome_detail.html"


class PlanetariumDomeCreateView(LoginRequiredMixin, generic.CreateView):
    model = PlanetariumDome
    fields = '__all__'
    template_name = "planetarium_domes/planetarium_dome_form.html"
    success_url = reverse_lazy("core_app:planetariumdomes-list")

class AstronomyShowListView(LoginRequiredMixin, generic.ListView):
    model = AstronomyShow
    context_object_name = "astronomy_shows"
    template_name = "astronomy_shows/astronomy_shows_list.html"
    paginate_by = 3


class AstronomyShowDetailView(LoginRequiredMixin, generic.DetailView):
    model = AstronomyShow
    queryset = AstronomyShow.objects.prefetch_related(
        "show_sessions", "show_sessions__planetarium_dome"
    )
    context_object_name = "astronomy_show"
    template_name = "astronomy_shows/astronomy_show_detail.html"

class AstronomyShowCreateView(LoginRequiredMixin, generic.CreateView):
    model = AstronomyShow
    fields = '__all__'
    template_name = "astronomy_shows/astronomy_show_form.html"
    success_url = reverse_lazy("astronomy:astronomy_shows_list.html")