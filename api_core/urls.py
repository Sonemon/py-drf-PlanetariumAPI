from django.urls import path, include
from rest_framework.routers import DefaultRouter

from api_core.views import (
    ShowThemeViewSet,
    AstronomyShowViewSet,
    PlanetariumDomeViewSet,
    ReservationViewSet,
    ShowSessionViewSet,
    TicketViewSet
)

router = DefaultRouter()
router.register("themes", ShowThemeViewSet)
router.register("shows", AstronomyShowViewSet)
router.register("domes", PlanetariumDomeViewSet)
router.register("reservations", ReservationViewSet, basename="reservation")
router.register("sessions", ShowSessionViewSet)
router.register("tickets", TicketViewSet, basename="ticket")

urlpatterns = [
    path("", include(router.urls)),
]
