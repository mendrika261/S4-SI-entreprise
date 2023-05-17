from django.contrib.auth.decorators import login_required
from django.shortcuts import render

from comptable.models import Exercice


@login_required
def bilan_actif(request, exercice_id=None):
    if exercice_id:
        exercice = Exercice.objects.get(id=exercice_id)
    elif request.POST.get('exercice_id'):
        exercice = Exercice.objects.get(id=request.POST.get('exercice_id'))
    else:
        exercice = Exercice.get_current()
    exercice_avant = Exercice.get_before_current()
    context = exercice.get_actif()
    context['exercice'] = exercice
    context['exercices'] = Exercice.objects.all().order_by('-debut')
    context['exercice_actuel'] = Exercice.get_current()
    return render(request, 'etat_financier/bilan_actif.html', context)


@login_required
def bilan_passif(request, exercice_id=None):
    if exercice_id:
        exercice = Exercice.objects.get(id=exercice_id)
    elif request.POST.get('exercice_id'):
        exercice = Exercice.objects.get(id=request.POST.get('exercice_id'))
    else:
        exercice = Exercice.get_current()
    exercice_avant = Exercice.get_before_current()
    context = exercice.get_passif()
    context['exercice'] = exercice
    context['exercices'] = Exercice.objects.all().order_by('-debut')
    context['exercice_actuel'] = Exercice.get_current()
    return render(request, 'etat_financier/bilan_passif.html', context)


@login_required
def bilan_resultat(request,exercice_id=None):
    if exercice_id:
        exercice = Exercice.objects.get(id=exercice_id)
    elif request.POST.get('exercice_id'):
        exercice = Exercice.objects.get(id=request.POST.get('exercice_id'))
    else:
        exercice = Exercice.get_current()
    exercice_avant = Exercice.get_before_current()

    context=exercice.get_resultat()
    context['exercice'] = exercice
    context['exercice_avant'] = exercice_avant
    context['exercices'] = Exercice.objects.all().order_by('-debut')
    context['exercice_actuel'] = Exercice.get_current()
    return render(request, 'etat_financier/bilan_resultat.html', context)
