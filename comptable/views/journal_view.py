import locale
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.db import IntegrityError, transaction
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render, get_object_or_404, redirect

from comptable.models import Journal, CompteGeneral, Devise, Piece, EcritureJournal, CompteTiers


@login_required
def choix_journal(request):
    context = {
        'liste_journal': Journal.objects.order_by('code')
    }
    return render(request, 'journal/choix_journal.html', context)


@login_required
@transaction.atomic
def add_journal(request, id_journal):
    journal = Journal.objects.get(id=id_journal)
    context = {
        'journal': journal,
        'prefixe_piece': Journal.objects.order_by('code'),
        'compte_general': CompteGeneral.objects.order_by('code'),
        'devises': Devise.objects.order_by('nom'),

    }

    if request.method == 'POST':
        list_row = request.POST['rows'].split(',')
        ecritures = []
        try:
            for row in list_row:
                try:
                    piece = Piece.objects.get(
                        prefixe=get_object_or_404(Journal, code=request.POST['prefixe_piece' + str(row)]),
                        numero=request.POST['numero_piece' + str(row)].strip())
                    created = False
                except Piece.DoesNotExist:
                    created = True
                    piece = Piece.objects.create(
                        prefixe=get_object_or_404(Journal, code=request.POST['prefixe_piece' + str(row)]),
                        numero=request.POST['numero_piece' + str(row)].strip(),
                    )
                ecritures.append(EcritureJournal.objects.create(
                    journal=get_object_or_404(Journal, pk=id_journal),
                    date=request.POST['date' + str(row)],
                    piece=piece,
                    compte_general=get_object_or_404(CompteGeneral, pk=request.POST['compte_general' + str(row)]),
                    compte_tiers=CompteTiers.objects.get(
                        pk=request.POST['compte_tiers' + str(row)]) if request.POST.get(
                        'compte_tiers' + str(row)) else None,
                    intitule=request.POST['intitule' + str(row)],
                    devise=get_object_or_404(Devise, pk=request.POST['devise' + str(row)]),
                    debit=request.POST['debit' + str(row)] if request.POST['debit' + str(row)] != '' else 0,
                    credit=request.POST['credit' + str(row)] if request.POST['credit' + str(row)] != '' else 0,
                ))
                if created:
                    context['warnings'] = [f'La pièce {piece} n\'existe pas, elle a été créée automatiquement']
                context['success'] = ['Ecriture enregistrée avec succès']
        except ValidationError as e:
            context['errors'] = e.messages
        except Exception:
            context['errors'] = ['Une erreur est survenue']
        # verify sum debit = sum credit
        if sum([float(e.debit) for e in ecritures]) != sum([float(e.credit) for e in ecritures]):
            context['errors'] = ['La somme des débits doit être égale à la somme des crédits']
    return render(request, 'journal/ecriture_journal.html', context)


@login_required
def get_grand_livre(request):
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    # 'mois': [date(2000, i, 1).strftime('%B').title() for i in range(1, 13)],
    context = {
        'compte_general': CompteGeneral.objects.order_by('code'),
        'compte_tiers': CompteTiers.objects.order_by('code'),
        'mois': [str(i) for i in range(1, 13)],
        'annee': [str(i) for i in range(2023, 2024)]
    }

    if request.method == 'POST':
        livre = EcritureJournal.objects.filter(
            date__year=request.POST['annee'].strip(),
            date__month=request.POST['mois'].strip(),
        ).order_by('date')
        if request.POST['compte_general'] != '':
            livre = livre.filter(compte_general_id=request.POST['compte_general'].strip())
        if request.POST['compte_tiers'] != '':
            livre = livre.filter(compte_tiers_id=request.POST['compte_tiers'].strip())
        context['livre'] = livre
        context['filtre'] = request.POST
        context['filtre_compte_general'] = int(request.POST['compte_general'].strip()) if request.POST['compte_general'] != '' else None
        context['filtre_compte_tiers'] = int(request.POST['compte_tiers'].strip()) if request.POST['compte_tiers'] != '' else None
        context['s_debit'] = livre.aggregate(Sum('debit'))['debit__sum'] if livre.aggregate(Sum('debit'))['debit__sum'] else 0
        context['s_credit'] = livre.aggregate(Sum('credit'))['credit__sum'] if livre.aggregate(Sum('credit'))['credit__sum'] else 0
        context['s_diff'] = abs(context['s_debit'] - context['s_credit'])

    return render(request, 'journal/grand_livre.html', context)


@login_required
def get_balance(request):
    context = {}
    if request.method == 'POST':
        date = request.POST['date'].split(' - ')
        debut = datetime.strptime(date[0], '%m/%d/%Y').date()
        fin = datetime.strptime(date[1], '%m/%d/%Y').date()
        result = []
        comptes = CompteGeneral.objects.order_by('code')
        for compte in comptes:
            ecritures = EcritureJournal.objects.filter(
                date__gte=debut,
                date__lte=fin,
                compte_general_id=compte.id,
            ).order_by('date')
            somme_debit = ecritures.aggregate(Sum('debit'))['debit__sum'] if ecritures.aggregate(Sum('debit'))['debit__sum'] else 0
            somme_credit = ecritures.aggregate(Sum('credit'))['credit__sum'] if ecritures.aggregate(Sum('credit'))['credit__sum'] else 0
            solde_debit = somme_debit - somme_credit
            solde_credit = somme_credit - somme_debit
            result.append({
                'compte': compte,
                'somme_debit': somme_debit,
                'somme_credit': somme_credit,
                'solde_debit': solde_debit,
                'solde_credit': solde_credit,
            })
        context['date'] = request.POST['date']
        context['result'] = result
    return render(request, 'journal/balance.html', context)


@login_required
def view_ecriture(request, id_piece):
    try:
        context = {
            'ecritures': EcritureJournal.objects.filter(piece_id=id_piece).order_by('date'),
            'intitule': EcritureJournal.objects.filter(piece_id=id_piece).first().intitule,
            'piece': EcritureJournal.objects.filter(piece_id=id_piece).first().piece,
            'date': EcritureJournal.objects.filter(piece_id=id_piece).first().date,
        }
    except Piece.DoesNotExist:
        raise Http404(f"La pièce { id_piece } n'existe pas")
    return render(request, 'journal/view_ecriture.html', context)
