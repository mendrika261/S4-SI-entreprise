from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from comptable.models import Exercice

nom_simple = 'exercice'
nom_avec_article = 'un exercice'
nom_avec_article_def = "l'exercice"

template_form = 'exercice/form.html'
list_template = 'exercice/list.html'


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
            Exercice.create(request.POST['debut'], request.POST['fin'])
            # FIN
            context['success'] = [nom_avec_article_def + ' a été créé avec succès']
        except ValidationError as e:
            # DEBUT TODO
            context['debut'] = request.POST['debut']
            context['fin'] = request.POST['fin']
            context['errors'] = e.messages
            # FIN
    return render(request, template_form, context)


@login_required
def update(request, id_object):
    # DEBUT TODO
    object_i = get_object_or_404(Exercice, pk=id_object)
    context = {
        'exercice': object_i.id,
        'debut': object_i.debut,
        'fin': object_i.fin,
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
                'debut': request.POST['debut'],
                'fin': request.POST['fin']
            })
            object_i.update(request.POST['debut'], request.POST['fin'])
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
    object_i = get_object_or_404(Exercice, pk=id_object)
    # FIN
    object_i.remove()
    context['success'] = [nom_avec_article_def + ' a été supprimé avec succès']
    return redirect('list_' + nom_simple)


@login_required
def read(request):
    # DEBUT TODO
    context = {nom_simple + 's': Exercice.objects.all()}

    # FIN
    return render(request, list_template, context)
