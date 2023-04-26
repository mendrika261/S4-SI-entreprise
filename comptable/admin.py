from django.contrib import admin

from comptable.models import HistoriqueSociete, Log

admin.site.register(HistoriqueSociete)
admin.site.register(Log)
