from django.shortcuts import render

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


# handle 404 error
def error_404(request, exception=None, template_name="base/404.html"):
    return render(request, template_name, status=404)

