from django.shortcuts import render
from django.views.decorators.csrf import requires_csrf_token

from ..models import HistoriqueSociete, Menu


def global_view(request):
    societe = HistoriqueSociete.get_last_information()
    context = {
        'societe': societe,
        'title': societe.nom.title(),
        'menu': Menu.get_menu(),
        'theme': 'light',
        'theme_color': 'teal',
        'theme_accent': 'info',
        'request_method': request.method,
    }
    return context


@requires_csrf_token
def custom_404_view(request, exception):
    return render(request, 'base/404.html', status=404, context={'status': 404})

