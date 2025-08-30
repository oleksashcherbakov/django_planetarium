from django.contrib.auth.models import User
from django.db import models


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
    show_sessions = models.ForeignKey(ShowSession)
    reserve = models.ForeignKey(
        "Reservation", on_delete=models.CASCADE, related_name="tickets"
    )

    class Meta:
        unique_together = ("row", "seat", "show_sessions")

    def __str__(self):
        return f"{self.row} {self.seat} {self.show_sessions.planetarium_dome}"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    ticket = models.ForeignKey(Ticket, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.ticket} {self.created_at}"


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
