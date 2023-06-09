from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.utils.timezone import now

from comptable.models import Produit, Centre

nom_simple = 'produit'
nom_avec_article = 'un produit'
nom_avec_article_def = 'le produit'

template_form = 'produit/form.html'
list_template = 'produit/list.html'


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
            Produit.create(request.POST['nom'], request.POST['prix'], request.POST['unite'], request.POST['stock'])
            # FIN
            context['success'] = [nom_avec_article_def + ' a été créé avec succès']
        except ValidationError as e:
            context['nom'] = request.POST['nom']
            context['prix'] = request.POST['prix']
            context['unite'] = request.POST['unite']
            context['stock'] = request.POST['stock']
            context['errors'] = e.messages
    return render(request, template_form, context)


@login_required
def update(request, id_object):
    # DEBUT TODO
    object_i = get_object_or_404(Produit, pk=id_object)
    context = {
        'nom': object_i.nom,
        'prix': object_i.prix,
        'unite': object_i.unite,
        'stock': object_i.stock,
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
                'prix': request.POST['prix'],
                'unite': request.POST['unite'],
                'stock': request.POST['stock'],
            })
            object_i.update(request.POST['nom'], request.POST['prix'], request.POST['unite'], request.POST['stock'])
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
    object_i = get_object_or_404(Produit, pk=id_object)
    # FIN
    object_i.remove()
    context['success'] = [nom_avec_article_def + ' a été supprimé avec succès']
    return redirect('list_' + nom_simple)


@login_required
def read(request):
    # DEBUT TODO
    context = {nom_simple + 's': Produit.objects.all()}
    # FIN
    return render(request, list_template, context)


@login_required
def analytique_produit(request, id_produit):
    if not id_produit:
        return redirect('list_' + nom_simple)
    produit = get_object_or_404(Produit, pk=id_produit)
    context = {
        'produit': produit,
        'compte_charges': produit.get_compte_non_null(),
        'centres': Centre.objects.order_by('nom'),
        'date_query': now()
    }
    return render(request, 'analyse/produit.html', context)
