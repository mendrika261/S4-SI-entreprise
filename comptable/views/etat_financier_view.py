from django.db.models import Sum
from django.shortcuts import render

from comptable.models import Exercice, EcritureJournal


def get_value(compte_general_id):
    credit = EcritureJournal.objects.filter(compte_general__id=compte_general_id).aggregate(Sum('credit'))['credit__sum']
    debit = EcritureJournal.objects.filter(compte_general__id=compte_general_id).aggregate(Sum('debit'))['debit__sum']
    if credit is None:
        credit = 0
    if debit is None:
        debit = 0
    return abs(credit - debit)


def get_total_actif_non_courant():
    total = 0
    total += get_value(20)
    total += get_value(21)
    total += get_value(22)
    total += get_value(23)
    total += get_value(25)
    total += get_value(13)
    return total


def get_total_actif_courant():
    total = 0
    total += get_value(3)
    total += get_value(4)
    total += get_value(5)
    return total

def bilan_actif(request):
    context = {
        'exercice': Exercice.get_current(),
        'capital': get_value(10100),
        'immobilisation_incorporelle': get_value(20),
        'immobilisation_corporelle': get_value(21),
        'immobilisation_biologique': get_value(22),
        'immobilisation_en_cours': get_value(23),
        'immobilisation_financiere': get_value(25),
        'impot_differe': get_value(13),
        'stocks': get_value(3),
        'creances': get_value(4),
        'tresorerie': get_value(5),
        'total_actif_courant': get_total_actif_courant(),
        'total_actif_non_courant': get_total_actif_non_courant(),
        'total_actif': get_total_actif_courant() + get_total_actif_non_courant(),
    }
    return render(request, 'etat_financier/bilan_actif.html', context)
