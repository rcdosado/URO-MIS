from django.contrib import admin
from .models import Presentation, Organizer


class PresentationAdmin(admin.ModelAdmin):
    class Meta:
        model = Presentation


admin.site.register(Presentation, PresentationAdmin)


class OrganizerAdmin(admin.ModelAdmin):
    class Meta:
        model = Organizer

admin.site.register(Organizer, OrganizerAdmin)

