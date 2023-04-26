from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.shortcuts import render, redirect
from comptable.models import HistoriqueSociete, Log, StatusEntreprise, Devise


@login_required
def afficher(request):
    historiques = Log.objects.order_by('-date')
    context = {
        'historiques': historiques,
    }
    return render(request, 'historique_societe/historique.html', context)


@login_required
def modification(request):
    historique = HistoriqueSociete.get_last_information()
    context = {
        'historique': historique,
        'status_entreprise': StatusEntreprise.objects.order_by('sigle'),
        'devises': Devise.objects.order_by('code')
    }
    if request.method == 'POST':
        try:
            historique = HistoriqueSociete.create_wt_file(
                request.POST['nom'],
                request.POST['objectif'],
                request.POST['siege'],
                request.POST['status_entreprise'],
                request.POST['nif'],
                request.POST['stat'],
                request.POST['reg_commerce'],
                request.POST['devise_compte']
            )
            context['success'] = ["Les informations ont été modifiées avec succès"]
            context['historique'] = historique
        except ValidationError as e:
            context['errors'] = e.messages
    return render(request, 'historique_societe/form.html', context)


@login_required
def import_fichier(request):
    context = {
        'historiques': Log.objects.order_by('-date'),
    }
    if request.method == 'POST':
        try:
            HistoriqueSociete.import_file(request.POST['type'], request.FILES['file'])
            context['success'] = ['Le fichier a été bien importé']
        except ValidationError as e:
            context['errors'] = e.messages
        """except Exception:
            context['errors'] = ["Le traitement du fichier a échoué! <br> Vérifier que le fichier est un .pdf ou "
                                 "un fichier image après avoir sélectionner le type"]"""
    else:
        return redirect('historique_societe')
    return render(request, 'historique_societe/historique.html', context)
