from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now

from comptable.models import Centre, Produit

nom_simple = 'centre'
nom_avec_article = 'un centre'
nom_avec_article_def = 'le centre'

template_form = 'centre/form.html'
list_template = 'centre/list.html'


@login_required
def create(request):
    context = {
        'title': 'Ajouter ' + nom_avec_article,
        'action': 'Ajouter',
        'icon': 'fas fa-save',
        'color': 'success',
        'categories': Centre.CATEGORY,
    }
    if request.method == 'POST':
        try:
            # DEBUT TODO
            Centre.create(request.POST['nom'], request.POST['categorie'])
            # FIN
            context['success'] = [nom_avec_article_def + ' a été créé avec succès']
        except ValidationError as e:
            context['nom'] = request.POST['nom']
            context['categorie'] = request.POST['categorie']
            context['errors'] = e.messages
    return render(request, template_form, context)


@login_required
def update(request, id_object):
    # DEBUT TODO
    object_i = get_object_or_404(Centre, pk=id_object)
    context = {
        'nom': object_i.nom,
        'categorie': object_i.categorie,
        'categories': Centre.CATEGORY,
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
                'nom': request.POST['nom'],
                'categorie': request.POST['categorie'],
            })
            object_i.update(request.POST['nom'], request.POST['categorie'])
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
    object_i = get_object_or_404(Centre, pk=id_object)
    # FIN
    object_i.remove()
    context['success'] = [nom_avec_article_def + ' a été supprimé avec succès']
    return redirect('list_' + nom_simple)


@login_required
def read(request):
    # DEBUT TODO
    context = {nom_simple + 's': Centre.objects.all()}
    # FIN
    return render(request, list_template, context)


@login_required
def analytique_centre(request, id_centre):
    if not id_centre:
        return redirect('list_' + nom_simple)
    centre = get_object_or_404(Centre, pk=id_centre)
    context = {
        'centre': centre,
        'produits': Produit.objects.order_by('nom'),
        'centres': Centre.objects.order_by('nom'),
        'date_query': now()
    }
    return render(request, 'analyse/centre.html', context)
