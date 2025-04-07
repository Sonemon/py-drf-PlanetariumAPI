from django.contrib import admin
from api_core.models import(
    Ticket,
    ShowTheme,
    ShowSession,
    Reservation,
    PlanetariumDome,
    AstronomyShow
)


admin.site.register(Ticket)
admin.site.register(ShowTheme)
admin.site.register(ShowSession)
admin.site.register(Reservation)
admin.site.register(PlanetariumDome)
admin.site.register(AstronomyShow)
