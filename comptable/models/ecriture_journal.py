from datetime import datetime

from django.core.exceptions import ValidationError
from django.db import models, transaction

from . import Devise, CompteGeneral, CompteTiers


class EcritureJournal(models.Model):
    exercice = models.ForeignKey('Exercice', on_delete=models.CASCADE)
    journal = models.ForeignKey('Journal', on_delete=models.CASCADE)
    date = models.DateField()
    piece = models.ForeignKey('Piece', on_delete=models.CASCADE)
    compte_general = models.ForeignKey('CompteGeneral', on_delete=models.CASCADE)
    compte_tiers = models.ForeignKey('CompteTiers', on_delete=models.CASCADE, null=True, default=None)
    intitule = models.CharField(max_length=100)
    devise = models.ForeignKey(Devise, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    credit = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    valide = models.DateField(null=True)

    def __str__(self):
        return str(self.compte_general) + " - " + self.intitule

    # Setters
    def set_exercice(self, exercice_id):
        try:
            from comptable.models import Exercice
            self.exercice = Exercice.objects.get(id=exercice_id)
        except Exception:
            raise ValidationError('L\'exercice n\'existe pas')

    def set_journal(self, journal_id):
        try:
            from comptable.models import Journal
            self.journal = Journal.objects.get(id=journal_id)
        except Exception:
            raise ValidationError('Le journal n\'existe pas')

    def set_date(self, date):
        if date == '' or date is None:
            raise ValidationError('La date ne peut pas être vide')
        try:
            self.date = datetime.strptime(date, '%d/%m/%Y')
        except Exception:
            raise ValidationError('La date n\'est pas au bon format dd/mm/aaaa')

    def set_piece(self, piece_id):
        try:
            from comptable.models import Piece
            self.piece = Piece.objects.get(id=piece_id)
        except Exception:
            raise ValidationError('La pièce n\'existe pas')

    def set_compte_general(self, compte_general_id):
        try:
            self.compte_general = CompteGeneral.objects.get(id=compte_general_id)
        except Exception:
            raise ValidationError('Le compte général n\'existe pas')

    def set_compte_tiers(self, compte_tiers_id):
        try:
            self.compte_tiers = CompteTiers.objects.get(id=compte_tiers_id)
        except Exception:
            raise ValidationError('Le compte tiers n\'existe pas')

    def set_intitule(self, intitule):
        if intitule == '' or intitule is None:
            raise ValidationError('L\'intitulé ne peut pas être vide')
        if len(str(intitule)) > 100:
            raise ValidationError('L\'intitulé ne peut pas dépasser 100 caractères')
        self.intitule = intitule

    def set_devise(self, devise_id):
        try:
            self.devise = Devise.objects.get(id=devise_id)
        except Exception:
            raise ValidationError('La devise n\'existe pas')

    def set_debit(self, debit):
        if debit == '' or debit is None:
            raise ValidationError('Le débit ne peut pas être vide')
        try:
            self.debit = float(debit)
            if debit < 0:
                raise ValidationError('Le débit doit être positif')
        except Exception:
            raise ValidationError('Le débit doit être un nombre')

    def set_credit(self, credit):
        if credit == '' or credit is None:
            raise ValidationError('Le crédit ne peut pas être vide')
        try:
            self.credit = float(credit)
            if credit < 0:
                raise ValidationError('Le crédit doit être positif')
        except Exception:
            raise ValidationError('Le crédit doit être un nombre')

    # Methods
    @staticmethod
    @transaction.atomic
    def create(journal_id, piece_id, compte_general_id, compte_tiers_id, intitule, devise_id, debit, credit, date):
        ecriture = EcritureJournal()

        from comptable.models import Exercice
        exercice = Exercice.get_current()
        ecriture.set_exercice(exercice)

        ecriture.set_journal(journal_id)
        ecriture.set_piece(piece_id)
        ecriture.set_compte_general(compte_general_id)

        if compte_tiers_id != '' or compte_tiers_id is not None:
            if CompteTiers.objects.filter(compte_general=ecriture.compte_general, id=compte_tiers_id).count() == 0:
                raise ValidationError(f'Le compte tiers #{compte_tiers_id} n\'est pas associé au compte général '
                                      f'{ecriture.compte_general}')
            ecriture.set_compte_tiers(compte_tiers_id)

        ecriture.set_intitule(intitule)
        ecriture.set_devise(devise_id)
        ecriture.set_debit(debit)
        ecriture.set_credit(credit)
        ecriture.set_date(date)
        ecriture.save()
        return ecriture

    @staticmethod
    def import_from_csv(file):
        import csv
        try:
            with open(file, 'r') as f:
                reader = csv.reader(f)
                next(reader)
                for row in reader:
                    try:
                        EcritureJournal.create(row[0], row[1], row[2], row[3], row[4], row[5], row[6], row[7], row[8])
                    except ValidationError as e:
                        raise ValidationError("Erreur lors de l'importation à la ligne " + str(row) + " : \n" + str(e))
        except FileNotFoundError:
            raise ValidationError("Le traitement du fichier a échoué")
        return 0
