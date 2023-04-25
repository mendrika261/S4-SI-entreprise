from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from comptable.models import Piece, Journal

nom_simple = 'piece'
nom_avec_article = 'une piece'
nom_avec_article_def = 'la piece'

template_form = 'piece/form.html'
list_template = 'piece/list.html'


@login_required
def create(request):
    context = {
        'title': 'Ajouter ' + nom_avec_article,
        'action': 'Ajouter',
        'icon': 'fas fa-save',
        'color': 'success',
        'code_journals': Journal.objects.order_by('code')
    }
    if request.method == 'POST':
        try:
            # DEBUT TODO
            Piece.create(request.POST['prefixe'], request.POST['numero'])
            # FIN
            context['success'] = [nom_avec_article_def + ' a été créé avec succès']
        except ValidationError as e:
            context['prefixe'] = request.POST['prefixe']
            context['numero'] = request.POST['numero']
            context['errors'] = e.messages
    return render(request, template_form, context)


@login_required
def update(request, id_object):
    # DEBUT TODO
    object_i = get_object_or_404(Piece, pk=id_object)
    context = {
        'piece': object_i.id,
        'prefixe': object_i.prefixe,
        'numero': object_i.numero,
        'code_journals': Journal.objects.order_by('code')
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
                'prefixe': request.POST['prefixe'],
                'numero': request.POST['numero']
            })
            object_i.update(request.POST['prefixe'], request.POST['numero'])
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
    object_i = get_object_or_404(Piece, pk=id_object)
    # FIN
    object_i.remove()
    context['success'] = [nom_avec_article_def + ' a été supprimé avec succès']
    return redirect('list_' + nom_simple)


@login_required
def read(request):
    # DEBUT TODO
    context = {nom_simple + 's': Piece.objects.all()}

    # FIN
    return render(request, list_template, context)
