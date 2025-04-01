from datetime import timedelta

from rest_framework import serializers
from django.utils import timezone
from django.contrib.auth.models import User
from api_core.models import (
    Ticket,
    ShowTheme,
    ShowSession,
    Reservation,
    PlanetariumDome,
    AstronomyShow
)


class AstronomyShowSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = AstronomyShow
        fields = ["id", "title", "description"]


class ShowThemeListSerializer(serializers.ModelSerializer):
    class Meta:
        model = ShowTheme
        fields = ["id", "name"]

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters")
        if ShowTheme.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("This theme already exists")

        return value


class ShowThemeDetailSerializer(serializers.ModelSerializer):
    shows = serializers.SerializerMethodField()

    class Meta:
        model = ShowTheme
        fields = ["id", "name", "shows"]

    def get_shows(self, obj):
        shows = obj.shows.all()
        return AstronomyShowSimpleSerializer(shows, many=True).data


class AstronomyShowSerializer(serializers.ModelSerializer):
    themes = ShowThemeListSerializer(many=True)

    class Meta:
        model = AstronomyShow
        fields = ["id", "title", "description", "themes"]

    def validate_title(self, value):
        value = value.strip()

        if len(value) < 5:
            raise serializers.ValidationError("Title must be at least 5 characters")
        if AstronomyShow.objects.filter(title__iexact=value).exists():
            raise serializers.ValidationError("This show already exists")

        return value


class PlanetariumDomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = PlanetariumDome
        fields = ["id", "name", "rows", "seats_in_row", "capacity"]

    def validate_name(self, value):
        value = value.strip()

        if len(value) < 3:
            raise serializers.ValidationError("Name must be at least 3 characters")
        if PlanetariumDome.objects.filter(name__iexact=value).exists():
            raise serializers.ValidationError("This dome already exists")

        return value

    def validate_rows(self, value):
        if value <= 0:
            raise serializers.ValidationError("Number of rows must be greater than 0")
        return int(value)

    def validate_seats_in_row(self, value):
        if value <= 0:
            raise serializers.ValidationError("Number of seats per row must be greater than 0")
        return int(value)


class ShowSessionSerializer(serializers.ModelSerializer):
    astronomy_show_title = serializers.CharField(source="astronomy_show.title", read_only=True)
    planetarium_dome_name = serializers.CharField(source="planetarium_dome.name", read_only=True)
    available_seats = serializers.SerializerMethodField()

    class Meta:
        model = ShowSession
        fields = [
            "id",
            "astronomy_show",
            "astronomy_show_title",
            "planetarium_dome",
            "planetarium_dome_name",
            "show_time",
            "available_seats"
        ]

    def get_available_seats(self, obj):
        return obj.planetarium_dome.capacity - obj.tickets.count()

    def validate_show_time(self, value):
        if value < timezone.now():
            raise serializers.ValidationError("Show time cannot be in the past")
        return value

    def validate_astronomy_show(self, value):
        if not AstronomyShow.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Invalid astronomy show")
        return value

    def validate_planetarium_dome(self, value):
        if not PlanetariumDome.objects.filter(id=value.id).exists():
            raise serializers.ValidationError("Invalid planetarium dome")
        return value

    def validate(self, data):
        dome = data["planetarium_dome"]
        show_time = data["show_time"]
        default_duration = timedelta(minutes=30)

        overlapping_sessions = ShowSession.objects.filter(
            planetarium_dome=dome,
            show_time__range=(show_time - default_duration, show_time + default_duration)
        ).exists()

        if overlapping_sessions:
            raise serializers.ValidationError(
                "A session is already scheduled for this planetarium dome at the given time")

        return data


class TicketSerializer(serializers.ModelSerializer):
    show_session_info = serializers.SerializerMethodField()

    class Meta:
        model = Ticket
        fields = [
            "id",
            "row",
            "seat",
            "show_session",
            "show_session_info",
            "reservation",
        ]
        extra_kwargs = {
            "reservation": {"read_only": True}
        }

    def get_show_session_info(self, obj):
        return {
            "show_time": obj.show_session.show_time,
            "astronomy_show": obj.show_session.astronomy_show.title,
            "planetarium_dome": obj.show_session.planetarium_dome.name
        }

    def validate(self, data):
        if Ticket.objects.filter(
                show_session=data["show_session"],
                row=data["row"],
                seat=data["seat"]
        ).exists():
            raise serializers.ValidationError("This seat is already taken for this show session")

        show_session = data["show_session"]
        if (data["row"] > show_session.planetarium_dome.rows or
                data["seat"] > show_session.planetarium_dome.seats_in_row):
            raise serializers.ValidationError("Invalid seat number for this planetarium dome")

        return data


class ReservationSerializer(serializers.ModelSerializer):
    tickets = TicketSerializer(many=True, read_only=True)

    class Meta:
        model = Reservation
        fields = ["id", "created_at", "user", "tickets"]
        read_only_fields = ["created_at"]


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["username", "password", "email"]

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data["username"],
            password=validated_data["password"],
            email=validated_data.get("email", "")
        )
        return user
