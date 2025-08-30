from django.contrib import admin

from core_app.models import (
    ShowSession,
    Reservation,
    Ticket,
    PlanetariumDome,
    AstronomyShow,
    ShowTheme,
)


@admin.register(ShowSession)
class ShowSessionAdmin(admin.ModelAdmin):
    list_display = (
        "astronomy_show_id",
        "planetarium_dome_id",
        "show_time",
    )
    list_filter = ("astronomy_show_id", "planetarium_dome_id", "show_time")
    search_fields = ("show_time",)


@admin.register(Ticket)
class TicketAdmin(admin.ModelAdmin):
    list_display = (
        "row",
        "seat",
    )
    list_filter = (
        "row",
        "seat",
    )
    search_fields = (
        "row",
        "seat",
    )


@admin.register(Reservation)
class ReservationAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "ticket",
        "created_at",
    )
    list_filter = (
        "user",
        "created_at",
        "ticket",
    )
    search_fields = (
        "user__username",
        "user__email",
    )


@admin.register(PlanetariumDome)
class PlanetariumDomeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "rows",
        "seats_in_row",
    )


@admin.register(AstronomyShow)
class AstronomyShowAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "description",
    )
    list_filter = (
        "title",
        "description",
    )
    search_fields = (
        "title",
        "description",
    )


@admin.register(ShowTheme)
class ShowThemeAdmin(admin.ModelAdmin):
    list_display = ("name",)
    list_filter = ("name",)
    search_fields = ("name",)
