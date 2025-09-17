"""
URL configuration for djangoplanetarium project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path

from core_app.views import (
    index,
    show_themes_list_view,
    show_themes_detail,
    ShowSessionsListView,
    ShowSessionsDetailView,
    ShowSessionsCreateView,
    TicketListView,
    TicketDetailView,
    TicketCreateView,
    ReservationListView,
    ReservationDetailView,
    ReservationCreateView,
    PlanetariumDomeListView,
    PlanetariumDomeDetailView,
    PlanetariumDomeCreateView,
    AstronomyShowListView,
    AstronomyShowDetailView,
    AstronomyShowCreateView,
)


urlpatterns = [
    path("index/", index, name="index"),
    path("showthemes/", show_themes_list_view, name="showthemes-list"),
    path("showthemes/<int:pk>", show_themes_detail, name="showthemes-detail"),
    path("showsessions/", ShowSessionsListView.as_view(), name="showsessions-list"),
    path(
        "showsessions/<int:pk>",
        ShowSessionsDetailView.as_view(),
        name="showsessions-detail",
    ),
    path("showsessions/create", ShowSessionsCreateView.as_view(), name="showsessions-create"),
    path("tickets/", TicketListView.as_view(), name="tickets-list"),
    path("tickets/<int:pk>", TicketDetailView.as_view(), name="tickets-detail"),
    path("tickets/create", TicketCreateView.as_view(), name="tickets-create"),
    path("reservations/", ReservationListView.as_view(), name="reservations-list"),
    path(
        "reservations/<int:pk>",
        ReservationDetailView.as_view(),
        name="reservation-detail",
    ),
    path("reservations/create", ReservationCreateView.as_view(), name="reservations-create"),
    path(
        "planetariumdomes/",
        PlanetariumDomeListView.as_view(),
        name="planetariumdomes-list",
    ),
    path(
        "planetariumdomes/<int:pk>",
        PlanetariumDomeDetailView.as_view(),
        name="planetariumdome-detail",
    ),
    path("planetariumdomes/create", PlanetariumDomeCreateView.as_view(), name="planetariumdomes-create"),
    path(
        "astronomyshows/", AstronomyShowListView.as_view(), name="astronomyshows-list"
    ),
    path(
        "astronomyshows/<int:pk>",
        AstronomyShowDetailView.as_view(),
        name="astronomyshows-detail",
    ),
    path(
        "astronomyshows/create",
        AstronomyShowCreateView.as_view(),
        name="astronomyshows-create",
    ),
]


app_name = "core_app"
