from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse

from comptable.models import CompteGeneral

nom_simple = 'compte_general'
nom_avec_article = 'un compte général'
nom_avec_article_def = 'le compte général'

template_form = 'compte_general/form.html'
list_template = 'compte_general/list.html'


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
            CompteGeneral.create(request.POST['code'], request.POST['intitule'])
            # FIN
            context['success'] = [nom_avec_article_def + ' a été créé avec succès']
        except ValidationError as e:
            context['code'] = request.POST['code']
            context['intitule'] = request.POST['intitule']
            context['errors'] = e.messages
    return render(request, template_form, context)


@login_required
def update(request, id_object):
    # DEBUT TODO
    object_i = get_object_or_404(CompteGeneral, pk=id_object)
    context = {
        'code': object_i.code,
        'intitule': object_i.intitule
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
                'intitule': request.POST['intitule']
            })
            object_i.update(request.POST['code'], request.POST['intitule'])
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
    object_i = get_object_or_404(CompteGeneral, pk=id_object)
    # FIN
    object_i.remove()
    context['success'] = [nom_avec_article_def + ' a été supprimé avec succès']
    return redirect('list_' + nom_simple)


@login_required
def read(request):
    # DEBUT TODO
    context = {nom_simple + 's': CompteGeneral.objects.all()}
    # FIN
    return render(request, list_template, context)


@login_required
@transaction.atomic
def import_from_csv(request):
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage(location='csv_files/')
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)
            CompteGeneral.import_from_csv(file_path)
            context = {'success': ['Les comptes généraux ont été importés avec succès']}
        except ValidationError as e:
            context = {'errors': e.messages}
        except Exception:
            context = {'errors': ["Le traitement du fichier a échoué! <br> Vérifier que le fichier est un .csv et "
                                  "l'ordre des colonnes"]}
        return render(request, list_template, context)
    return render(request, list_template)
