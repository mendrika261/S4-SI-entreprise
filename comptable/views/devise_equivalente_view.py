from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from comptable.models import DeviseEquivalente, Devise

nom_simple = 'devise_equivalente'
nom_avec_article = 'une devise equivalente'
nom_avec_article_def = 'la devise equivalente'

template_form = 'devise_equivalente/form.html'
list_template = 'devise_equivalente/list.html'


@login_required
def create(request):
    context = {
        'title': 'Ajouter ' + nom_avec_article,
        'action': 'Ajouter',
        'icon': 'fas fa-save',
        'color': 'success',
        'devises': Devise.objects.order_by('code'),
    }
    if request.method == 'POST':
        try:
            # DEBUT TODO
            DeviseEquivalente.create(request.POST['devise'], request.POST['devise_equivalente'], request.POST['taux'])
            # FIN
            context['success'] = [nom_avec_article_def + ' a été créé avec succès']
        except ValidationError as e:
            context['devise'] = request.POST['devise']
            context['devise_equivalente'] = request.POST['devise_equivalente']
            context['taux'] = request.POST['taux']
            context['errors'] = e.messages
    return render(request, template_form, context)


@login_required
def update(request, id_object):
    # DEBUT TODO
    object_i = get_object_or_404(DeviseEquivalente, pk=id_object)
    context = {
        'devise': object_i.devise.id,
        'devise_equivalente': object_i.devise_equivalente.id,
        'taux': object_i.taux,
        'date': object_i.date,
        'devises': Devise.objects.order_by('nom'),
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
                'devise': int(request.POST['devise']),
                'devise_equivalente': int(request.POST['devise_equivalente']),
                'taux': request.POST['taux'],
            })
            object_i.update(request.POST['devise'], request.POST['devise_equivalente'], request.POST['taux'])
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
    object_i = get_object_or_404(DeviseEquivalente, pk=id_object)
    # FIN
    object_i.remove()
    context['success'] = [nom_avec_article_def + ' a été supprimé avec succès']
    return redirect('list_' + nom_simple)


@login_required
def read(request):
    # DEBUT TODO
    context = {nom_simple + 's': DeviseEquivalente.objects.all()}
    # FIN
    return render(request, list_template, context)
