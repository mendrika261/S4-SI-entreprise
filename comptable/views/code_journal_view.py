from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from comptable.models import Journal

nom_simple = 'journal'
nom_avec_article = 'un journal'
nom_avec_article_def = 'le journal'

template_form = 'code_journal/form.html'
list_template = 'code_journal/list.html'


@login_required
def create(request):
    context = {
        'title': 'Ajouter ' + nom_avec_article,
        'action': 'Ajouter',
        'icon': 'fas fa-save',
        'color': 'success',
    }
    if request.method == 'POST':
        try:
            # DEBUT TODO
            Journal.create(request.POST['code'], request.POST['nom'], request.POST['icon'], request.POST['color'])
            # FIN
            context['success'] = [nom_avec_article_def + ' a été créé avec succès']
        except ValidationError as e:
            context['code'] = request.POST['code']
            context['nom'] = request.POST['nom']
            context['icon_v'] = request.POST['icon']
            context['color_v'] = request.POST['color']
            context['errors'] = e.messages
    return render(request, template_form, context)


@login_required
def update(request, id_object):
    # DEBUT TODO
    object_i = get_object_or_404(Journal, pk=id_object)
    context = {
        'code': object_i.code,
        'nom': object_i.nom,
        'icon_v': object_i.icon,
        'color_v': object_i.color,
    }
    # FIN TODO
    if request.GET.get('remove') is not None:
        context.update({
            'title': 'Supprimer ' + nom_avec_article,
            'action': 'Confirmer la suppression',
            'form_action': "action='" + reverse('remove_' + nom_simple, args=[id_object]) + "'",
            'remove': True,
            'icon': 'fas fa-trash-alt',
            'color': 'danger',
        })
    else:
        context.update({
            'title': 'Modifier ' + nom_avec_article,
            'action': 'Modifier',
            'icon': 'fas fa-pencil-alt',
            'color': 'warning',
        })
    if request.method == 'POST':
        try:
            # DEBUT TODO
            context.update({
                'code': request.POST['code'],
                'nom': request.POST['nom'],
                'icon_v': request.POST['icon'],
                'color_v': request.POST['color'],
            })
            object_i.update(request.POST['code'], request.POST['nom'], request.POST['icon'], request.POST['color'])
            # FIN
            context['success'] = [nom_avec_article_def + ' a été modifié avec succès']
        except ValidationError as e:
            context['errors'] = e.messages
    return render(request, template_form, context)


@login_required
def remove(request, id_object):
    if request.method != 'POST':
        return redirect('list_' + nom_simple)
    context = {}
    # DEBUT TODO
    object_i = get_object_or_404(Journal, pk=id_object)
    # FIN
    object_i.remove()
    context['success'] = [nom_avec_article_def + ' a été supprimé avec succès']
    return redirect('list_' + nom_simple)


@login_required
def read(request):
    # DEBUT TODO
    context = {nom_simple + 's': Journal.objects.all()}
    # FIN
    return render(request, list_template, context)
