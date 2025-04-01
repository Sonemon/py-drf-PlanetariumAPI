from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from api_core.views import (
    ShowThemeViewSet,
    AstronomyShowViewSet,
    PlanetariumDomeViewSet,
    ReservationViewSet,
    ShowSessionViewSet,
    TicketViewSet,
    RegisterView,
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
    path("auth/login/", TokenObtainPairView.as_view(), name="login"),
    path("auth/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("auth/register/", RegisterView.as_view(), name="register")
]
