from django.contrib.auth.models import User
from django.db import models


class ShowTheme(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )

    def __str__(self):
        return self.name


class AstronomyShow(models.Model):
    title = models.CharField(
        max_length=255,
        unique=True,
    )
    description = models.TextField(blank=True, null=True)
    themes = models.ManyToManyField(
        ShowTheme,
        related_name="shows",
    )

    def __str__(self):
        return self.title


class PlanetariumDome(models.Model):
    name = models.CharField(
        max_length=255,
        unique=True,
    )
    rows = models.IntegerField()
    seats_in_row = models.IntegerField()

    @property
    def capacity(self):
        return self.rows * self.seats_in_row

    def __str__(self):
        return f"{self.name} ({self.rows} rows, {self.seats_in_row} seats)"


class Reservation(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User,
        related_name="reservations",
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Reservation for {self.user}"


class ShowSession(models.Model):
    astronomy_show = models.ForeignKey(
        AstronomyShow,
        related_name="sessions",
        on_delete=models.CASCADE,
    )
    planetarium_dome = models.ForeignKey(
        PlanetariumDome,
        related_name="sessions",
        on_delete=models.CASCADE,
     )
    show_time = models.DateTimeField(db_index=True)

    def __str__(self):
        return f"{self.astronomy_show.title} session at {self.show_time}"


class Ticket(models.Model):
    row = models.IntegerField()
    seat = models.IntegerField()
    show_session = models.ForeignKey(
        ShowSession,
        related_name="tickets",
        on_delete=models.CASCADE,
        db_index=True
    )
    reservation = models.ForeignKey(
        Reservation,
        related_name="tickets",
        on_delete=models.CASCADE,
        db_index=True,
        null=True,
        blank=True
    )

    class Meta:
        unique_together = ("show_session", "row", "seat")

    def __str__(self):
        return f"Ticket for {self.show_session.astronomy_show.title} at {self.show_session.show_time}"
