from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.db import models
from django.urls.base import reverse


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        "AstronomyShow", on_delete=models.CASCADE, related_name="show_sessions"
    )
    planetarium_dome = models.ForeignKey(
        "PlanetariumDome", on_delete=models.CASCADE, related_name="show_sessions"
    )
    show_time = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["show_time", "planetarium_dome"]

    def __str__(self):
        return f"{self.astronomy_show} {self.planetarium_dome}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_sessions = models.ForeignKey(ShowSession, on_delete=models.CASCADE)
    reserve = models.ForeignKey(
        "Reservation", on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        unique_together = ("row", "seat", "show_sessions")

    def __str__(self):
        return f"{self.row} {self.seat} {self.show_sessions}"

    def clean(self):
        dome = self.show_sessions.planetarium_dome

        if not (1 <= self.row <= dome.rows):
            raise ValidationError(f"row must be between 1 and {dome.rows}")

        if not (1 <= self.seat <= dome.seats_in_row):
            raise ValidationError(f"seat must be between 1 and {dome.seats_in_row}")

    def get_absolute_url(self):
        return reverse("core_app:tickets-detail", args=(str(self.id)))


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.created_at} by {self.user}"

    def get_absolute_url(self):
        return reverse("core_app:reservation-detail", args=(str(self.id)))


class PlanetariumDome(models.Model):
    name = models.CharField(max_length=100)
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    def __str__(self):
        return f"{self.name} {self.rows} {self.seats_in_row}"


class AstronomyShow(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    themes = models.ManyToManyField("ShowTheme", related_name="astronomy_shows")

    def __str__(self):
        return f"{self.title}"


class ShowTheme(models.Model):
    name = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return f"{self.name}"
