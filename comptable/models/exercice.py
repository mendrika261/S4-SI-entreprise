from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django.utils.timezone import now


class Exercice(models.Model):
    debut = models.DateField()
    fin = models.DateField()
    cloture = models.DateField(null=True)

    def __str__(self):
        return str(self.debut) + " à " + str(self.fin)

    # Setters
    def set_debut(self, debut):
        if debut == "" or debut is None:
            raise ValidationError("Vous devez taper une date de début")
        try:
            self.debut = debut
        except Exception:
            raise ValidationError("La forme de la date de début n'est pas valide")

    def set_fin(self, fin):
        if fin == "" or fin is None:
            raise ValidationError("Vous devez taper une date de fin ")
        if self.debut >= fin:
            raise ValidationError("La date de fin doit etre superieur a la date de debut")
        try:
            self.fin = fin
        except Exception:
            raise ValidationError("La forme de la date de fin n'est pas valide")

    # Methods
    @staticmethod
    def create(debut, fin):
        exercice = Exercice()
        exercice.set_debut(debut)
        exercice.set_fin(fin)
        exercice.save()
        return exercice

    def update(self, debut, fin):
        self.set_debut(debut)
        self.set_fin(fin)
        self.save()
        return self

    def remove(self):
        self.delete()
        return 0

    def close(self):
        self.cloture = now()
        self.save()
        return self

    @staticmethod
    def get_current():
        obj = Exercice.objects.filter(debut__lte=now(), fin__gte=now()).first()
        if obj is None or obj.cloture:
            raise ValidationError("Vous devez d'abord créer un exercice "
                                  "<a href='" + reverse('create_exercice') + "' class='text-bold'> Cliquer ici</a>")
        return obj

    @staticmethod
    def get_before_current():
        try:
            return Exercice.objects.filter(debut__lte=now(), fin__gte=now()).order_by('-debut')[1]
        except Exception:
            return None

    @staticmethod
    def get_compte(compte_general_code):
        from comptable.models import CompteGeneral
        return CompteGeneral.objects.filter(code__startswith=compte_general_code)

    def get_value(self, compte_general_code, actif=True):
        from comptable.models import EcritureJournal
        comptes = self.get_compte(compte_general_code)
        total = 0
        for compte in comptes:
            credit = EcritureJournal.objects.filter(exercice=self, compte_general=compte).aggregate(Sum('credit'))[
                'credit__sum']
            debit = EcritureJournal.objects.filter(exercice=self, compte_general=compte).aggregate(Sum('debit'))[
                'debit__sum']
            if credit is None:
                credit = 0
            if debit is None:
                debit = 0
            if actif and (debit - credit >= 0 or str(compte_general_code).startswith('2') or str(compte_general_code).startswith(
                    '3')):
                total += debit - credit
            elif not actif and debit - credit < 0:
                total += credit - debit
        return total

    def get_total(self, *compte_general_id, actif=True):
        total = 0
        for compte in compte_general_id:
            total += self.get_value(compte, actif)
        return total

    def get_actif(self):
        return {
            'capital': self.get_value(10100),

            'immobilisation_incorporelle': self.get_value(20),
            'ammortissement_incorporelle': abs(self.get_value(280)),
            'net_immobilisation_incorporelle': self.get_value(20) + self.get_value(280),

            'immobilisation_corporelle': self.get_value(21),
            'ammortissement_corporelle': abs(self.get_value(281)),
            'net_immobilisation_corporelle': self.get_value(21) + self.get_value(281),

            'immobilisation_biologique': self.get_value(22),
            'ammortissement_biologique': abs(self.get_value(282)),
            'net_immobilisation_biologique': self.get_value(22) + self.get_value(282),

            'immobilisation_en_cours': self.get_value(23),
            'ammortissement_en_cours': abs(self.get_value(283)),
            'net_immobilisation_en_cours': self.get_value(23),

            'immobilisation_financiere': self.get_value(25),
            'prov_immobilisation_financiere': abs(self.get_value(285)),
            'net_immobilisation_financiere': self.get_total(25, 285),

            'impot_differe': self.get_value(13),
            'net_impot_differe': self.get_value(13),

            'total_actif_non_courant': self.get_total(20, 21, 22, 23, 25, 13),
            'total_ammort_actif_non_courant': abs(self.get_total(280, 281, 282, 283, 285)),
            'total_actif_non_courant_net': self.get_total(20, 21, 22, 23, 25, 13, 280, 281, 282, 283, 285),

            # actif courant
            'stocks': self.get_total(32, 35, 37),
            'prov_pour_depreciation_stocks': abs(self.get_value(39)),
            'net_stocks': self.get_total(32, 35, 37, 39),

            'clients': self.get_value(41),
            'net_clients': self.get_value(41),

            'autres_creances': self.get_total(409, 467, 4457),
            'net_autres_creances': self.get_total(409, 467, 4457),

            'creances': self.get_total(41, 409, 467, 4457),
            'net_creances': self.get_total(41, 409, 467, 4457),

            'tresorerie': self.get_value(5),
            'net_tresorerie': self.get_value(5),

            'total_actif_courant': self.get_total(32, 35, 37, 41, 409, 467, 4457, 5),
            'total_prov_actif_courant': abs(self.get_total(39)),
            'total_actif_courant_net': self.get_total(32, 35, 37, 41, 409, 467, 4457, 5, 39),

            # total actif
            'total_actif': self.get_total(20, 21, 22, 23, 25, 13, 32, 35, 37, 41, 409, 467, 4457, 5),
            'total_ammort_actif': abs(self.get_total(280, 281, 282, 283, 285, 39)),
            'total_actif_net': self.get_total(20, 21, 22, 23, 25, 13, 32, 35, 37, 41, 409, 467, 4457, 5, 280, 281, 282,
                                              283, 285, 39),
        }

    def get_resultat(self):
        return {
            'chiffe_d_affaire': self.get_value(70, actif=False),
            'production_stockee': self.get_value(71, actif=False),
            'production_de_l_exercice': self.get_total(70, 71, actif=False),
            'achat_consommes': self.get_value(60),
            'services_exterieurs': self.get_total(61, 62),
            'consommation_de_l_exercice': self.get_total(60, 61, 62),
            'valeur_ajoutee_d_exploitation': self.get_total(70, 71, actif=False) - self.get_total(60, 61, 62),
            'charges_de_personnel': self.get_value(64),
            'impots': self.get_value(63),
            'excedent_brut': self.get_total(64, 63),
            'autres_produit': self.get_value(75, actif=False),
            'autres_charges': self.get_value(65),
            'dotations': self.get_value(68),
            'reprise': self.get_value(78, actif=False),
            'resultat_operationnel': self.get_total(75, 78, actif=False) + self.get_total(65, 68),
            'produits_financier': self.get_value(76, actif=False),
            'charges_financier': self.get_value(66),
            'resultat_financier': self.get_total(76, actif=False) + self.get_total(66),
            'resultat_avant_impot': (self.get_total(75, 78, actif=False) + self.get_total(65, 68)) - (self.get_total(76, actif=False) + self.get_total(66)),
            'impots_exigibles': self.get_value(695),
            'impots_differes': self.get_value(692),
            'resultat_net': self.get_total(695, 692),
            'elements_extraordinaire_produits': self.get_value(77, actif=False),
            'elements_extraordinaire_charges': self.get_value(67),
            'resultat_extraordinaire': self.get_total(77, actif=False) + self.get_total(67)
        }

    def get_passif(self):
        return {
            'capital': self.get_value(10, False),
            'reserve_legale':0,
            'resultat_en_instance':self.get_value(0, False),
            'resultat_net':self.get_value(12, False),
            'autres_capitaux_propres':self.get_value(11, False),

            #total des capitaux propres
            'total_capitaux': self.get_total(10, 12, 11, actif=False),

            #passifs non-courant
            'impots_differes': self.get_value(13, False),
            'emprunts_dettes': self.get_value(161, False),

            #total
            'total_passifs_non_courants':self.get_total(13, 161, actif=False),

            #passifs courants
            'emprunts_dettes_moins_1': 0,
            'dettes_court_terme':self.get_value(165, False),
            'fournisseurs':self.get_value(40, False),
            'avances_recues':self.get_value(49, False),
            'autres_dettes':self.get_total(42, 43, 44, actif=False),
            'comptes_et_tresorerie':self.get_value(5, False),

            #total passifs courants
            'total_passifs_courants':self.get_total(165, 40, 49, 42, 43, 44, 5, actif=False),

            #total des capitaux propres et passifs
            'total_capitaux_propres_passifs':self.get_total(10, 12, 11, 13, 161, 165, 40, 49, 42, 43, 44, 5, actif=False)
        }

    def get_value_by_name(self, name):
        values = self.get_actif()
        return values.get(name, 0)
