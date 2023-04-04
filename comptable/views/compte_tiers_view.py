from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from comptable.models import CompteTiers, CompteGeneral

nom_simple = 'compte_tiers'
nom_avec_article = 'un compte tiers'
nom_avec_article_def = 'le compte tiers'

template_form = 'compte_tiers/form.html'
list_template = 'compte_tiers/list.html'


@login_required
def create(request):
    context = {
        'title': 'Ajouter ' + nom_avec_article,
        'action': 'Ajouter',
        'icon': 'fas fa-save',
        'color': 'success',
        'compte_generals': CompteGeneral.objects.order_by('code'),
    }
    if request.method == 'POST':
        try:
            # DEBUT TODO
            CompteTiers.create(request.POST['compte_general'], request.POST['code'], request.POST['intitule'])
            # FIN
            context['success'] = [nom_avec_article_def + ' a été créé avec succès']
        except ValidationError as e:
            context['compte_general'] = request.POST['compte_general']
            context['code'] = request.POST['code']
            context['intitule'] = request.POST['intitule']
            context['errors'] = e.messages
    return render(request, template_form, context)


@login_required
def update(request, id_object):
    # DEBUT TODO
    object_i = get_object_or_404(CompteTiers, pk=id_object)
    context = {
        'compte_general': object_i.compte_general.id,
        'code': object_i.get_code(),
        'intitule': object_i.get_intitule(),
        'compte_generals': CompteGeneral.objects.order_by('code'),
    }
    # FIN TODO
    if request.GET.get('remove') is not None:
        context.update({
            'title': 'Supprimer ' + nom_avec_article,
            'action': 'Confirmer la suppression',
            'form_action': "action='" + reverse('remove_'+nom_simple, args=[id_object]) + "'",
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
                'compte_general': request.POST['compte_general'],
                'code': request.POST['code'],
                'intitule': request.POST['intitule']
            })
            object_i.update(request.POST['compte_general'], request.POST['code'], request.POST['intitule'])
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
    object_i = get_object_or_404(CompteTiers, pk=id_object)
    # FIN
    object_i.remove()
    context['success'] = [nom_avec_article_def + ' a été supprimé avec succès']
    return redirect('list_' + nom_simple)


@login_required
def read(request):
    # DEBUT TODO
    context = {nom_simple+'s': CompteTiers.objects.all()}
    # FIN
    return render(request, list_template, context)
