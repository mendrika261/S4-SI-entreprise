import locale
from datetime import datetime

from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.core.files.storage import FileSystemStorage
from django.db import transaction
from django.db.models import Sum
from django.http import Http404
from django.shortcuts import render

from comptable.models import Journal, CompteGeneral, Devise, Piece, EcritureJournal, CompteTiers, Exercice


@login_required
def choix_journal(request):
    context = {
        'liste_journal': Journal.objects.order_by('code'),
    }
    try:
        Exercice.get_current()
    except ValidationError as e:
        context['errors'] = e.messages
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
        'exercice': Exercice.get_current(),
    }

    if request.method == 'POST':
        try:
            debit_sum = 0
            credit_sum = 0
            for prefixe_piece, numero_piece, compte_general, compte_tiers, intitule, debit, credit, devise, date in \
                    zip(request.POST.getlist('prefixe_piece[]'), request.POST.getlist('numero_piece[]'),
                        request.POST.getlist('compte_general[]'), request.POST.getlist('compte_tiers[]'),
                        request.POST.getlist('intitule[]'), request.POST.getlist('debit[]'),
                        request.POST.getlist('credit[]'), request.POST.getlist('devise[]'),
                        request.POST.getlist('date[]')):

                prefixe = Journal.objects.get(id=prefixe_piece)
                if prefixe is None:
                    raise ValidationError(f'Le préfixe #{prefixe_piece} n\'existe pas')

                if Piece.objects.filter(prefixe=prefixe_piece, numero=numero_piece).count() == 0:
                    piece = Piece.create(prefixe.id, numero_piece)
                    context['warnings'] = [f'La pièce {piece} n\'existe pas, elle a été créée']
                else:
                    piece = Piece.objects.get(prefixe=prefixe, numero=numero_piece)
                piece_id = piece.id

                ecriture = EcritureJournal.create(
                    journal_id=journal.id,
                    piece_id=piece_id,
                    compte_general_id=compte_general,
                    compte_tiers_id=compte_tiers,
                    intitule=intitule,
                    debit=debit,
                    credit=credit,
                    devise_id=devise,
                    date=date
                )
                if ecriture is None:
                    raise ValidationError(f'L\'écriture {intitule} n\'a pas pu être créée')
                debit_sum += ecriture.debit
                credit_sum += ecriture.credit

            if debit_sum != credit_sum:
                raise ValidationError('La somme des débits doit être égale à la somme des crédits')

            context['success'] = ["L'écriture a été enregistrée dans l'exercice " + str(Exercice.get_current())]
        except ValidationError as e:
            context['errors'] = e.messages

    return render(request, 'journal/ecriture_journal.html', context)


@login_required
def get_grand_livre(request):
    locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    context = {
        'compte_general': CompteGeneral.objects.order_by('code'),
        'compte_tiers': CompteTiers.objects.order_by('code'),
        'mois': [str(i) for i in range(1, 13)],
        'annee': [str(i) for i in range(2023, 2024)]
    }

    if request.method == 'POST':
        if request.POST['compte_general'] == '':
            if request.POST['compte_tiers'] == '':
                context['errors'] = ['Veuillez sélectionner un compte!']
                return render(request, 'journal/grand_livre.html', context)

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
        context['filtre_compte_general'] = int(request.POST['compte_general'].strip()) \
            if request.POST['compte_general'] != '' else None
        context['filtre_compte_tiers'] = int(request.POST['compte_tiers'].strip()) \
            if request.POST['compte_tiers'] != '' else None
        context['s_debit'] = livre.aggregate(Sum('debit'))['debit__sum']\
            if livre.aggregate(Sum('debit'))['debit__sum'] else 0
        context['s_credit'] = livre.aggregate(Sum('credit'))['credit__sum']\
            if livre.aggregate(Sum('credit'))['credit__sum'] else 0
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
            somme_debit = ecritures.aggregate(Sum('debit'))['debit__sum'] if ecritures.aggregate(Sum('debit'))[
                'debit__sum'] else 0
            somme_credit = ecritures.aggregate(Sum('credit'))['credit__sum'] if ecritures.aggregate(Sum('credit'))[
                'credit__sum'] else 0
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
        raise Http404(f"La pièce {id_piece} n'existe pas")
    return render(request, 'journal/view_ecriture.html', context)


@login_required
@transaction.atomic
def import_from_csv(request):  # TODO
    if request.method == 'POST':
        try:
            uploaded_file = request.FILES['file']
            fs = FileSystemStorage(location='csv_files/')
            filename = fs.save(uploaded_file.name, uploaded_file)
            file_path = fs.path(filename)
            EcritureJournal.import_from_csv(file_path)
            context = {'success': ['Les comptes généraux ont été importés avec succès']}
        except ValidationError as e:
            context = {'errors': e.messages}
        return render(request, 'journal/choix_journal.html', context)
    return render(request, 'journal/choix_journal.html')
