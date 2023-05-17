from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.utils.timezone import now

from comptable.models import Centre


class Produit(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    unite = models.CharField(max_length=10)
    prix = models.DecimalField(max_digits=20, decimal_places=2)
    stock = models.DecimalField(max_digits=20, decimal_places=2, default=0)

    def __str__(self):
        return self.nom

    def set_nom(self, nom):
        if nom == '' or None:
            raise ValidationError('Le nom du produit ne peut pas être vide')
        try:
            self.nom = str(nom).capitalize()
        except IntegrityError:
            raise ValidationError('Le nom du produit doit être unique')

    def set_unite(self, unite):
        if unite == '' or None:
            raise ValidationError("L'unite ne peut pas être vide")
        self.unite = unite

    def set_prix(self, prix):
        if prix == '' or None:
            raise ValidationError("Le prix du produit ne peut pas être vide")
        self.prix = prix

    def set_stock(self, stock):
        self.stock = stock

    @staticmethod
    def create(nom, prix, unite, stock):
        produit = Produit()
        produit.set_nom(nom)
        produit.set_prix(prix)
        produit.set_unite(unite)
        produit.set_stock(stock)
        produit.save()
        return produit

    def update(self, nom, prix, unite, stock):
        self.set_nom(nom)
        self.set_prix(prix)
        self.set_unite(unite)
        self.set_stock(stock)
        self.save()
        return self

    def remove(self):
        self.delete()
        return 0

    def get_compte_non_null(self):
        from comptable.models import Analyse
        t = Analyse.objects.all()
        res = set()
        for x in t:
            res.add(x.ecriture.compte_general)
        """from comptable.models import CompteGeneral
        comptes = CompteGeneral.objects.filter(code__startswith='6')
        res = []
        for compte in comptes:
            if self.get_total_compte(compte.code) != 0:
                res.append(compte)"""
        return res

    def get_total_compte(self, code_compte, date=now()):
        from comptable.models import Analyse
        return Analyse.objects.filter(
            ecriture__compte_general__code=code_compte,
            ecriture__date__lte=date,
            produit__id=self.id).aggregate(models.Sum('valeur'))['valeur__sum'] or 0

    def get_compte_centre_pourcentage(self, code_compte, id_centre, date=now()):
        from comptable.models import Analyse
        compte_centre = Analyse.objects.filter(
            ecriture__compte_general__code=code_compte,
            ecriture__date__lte=date,
            centre__id=id_centre,
            produit__id=self.id).aggregate(models.Sum('valeur'))['valeur__sum'] or 0
        return compte_centre / self.get_total_compte(code_compte, date) * 100 if self.get_total_compte(code_compte, date) else 0

    def get_compte_centre_fixe(self, code_compte, id_centre, date=now()):
        from comptable.models import Analyse
        compte_centres = Analyse.objects.filter(
            ecriture__compte_general__code=code_compte,
            ecriture__date__lte=date,
            centre__id=id_centre,
            produit__id=self.id)
        somme_valeur = 0
        for compte_centre in compte_centres:
            somme_valeur += compte_centre.valeur * compte_centre.fixe / 100
        return somme_valeur

    def get_compte_centre_variable(self, code_compte, id_centre, date=now()):
        from comptable.models import Analyse
        compte_centres = Analyse.objects.filter(
            ecriture__compte_general__code=code_compte,
            ecriture__date__lte=date,
            centre__id=id_centre,
            produit__id=self.id)
        somme_valeur = 0
        for compte_centre in compte_centres:
            somme_valeur += compte_centre.valeur * compte_centre.variable / 100
        return somme_valeur

    def get_total(self, date=now()):
        from comptable.models import Analyse
        return Analyse.objects.filter(
            produit__id=self.id,
            ecriture__date__lte=date
        ).aggregate(models.Sum('valeur'))['valeur__sum'] or 0

    def total_fixe(self, id_centre, date=now()):
        total = 0
        for compte in self.get_compte_non_null():
            total += self.get_compte_centre_fixe(compte.code, id_centre, date)
        return total

    def total_variable(self, id_centre, date=now()):
        total = 0
        for compte in self.get_compte_non_null():
            total += self.get_compte_centre_variable(compte.code, id_centre, date)
        return total

    def total_centre(self, id_centre, date=now()):
        return self.total_fixe(id_centre, date) + self.total_variable(id_centre, date)

    def total_cout(self):
        return self.total_total_variable() + self.total_total_fixe()

    def prix_revient(self):
        try:
            return round(self.total_cout() / self.stock, 2)
        except Exception:
            return 0

    def rentabilite(self):
        try:
            return round(self.total_total_fixe() / (self.prix - (self.total_total_variable() / self.stock)), 2)
        except Exception:
            return 0

    def total_fixe_compte(self, code_compte, date=now()):
        total = 0
        for centre in Centre.objects.all():
            total += self.get_compte_centre_fixe(code_compte, centre.id, date)
        return total

    def total_variable_compte(self, code_compte, date=now()):
        total = 0
        for centre in Centre.objects.all():
            total += self.get_compte_centre_variable(code_compte, centre.id, date)
        return total

    def total_total_fixe(self, date=now()):
        total = 0
        for centre in Centre.objects.all():
            total += self.total_fixe(centre.id, date)
        return total

    def total_total_variable(self, date=now()):
        total = 0
        for centre in Centre.objects.all():
            total += self.total_variable(centre.id, date)
        return total

    def repartition_centre(self, centre_operationnel, centre_structure):
        from comptable.models import AnalyseStructure
        return AnalyseStructure.objects.filter(
                    produit=self,
                    centre_operationnel=centre_operationnel,
                    centre_structure=centre_structure
                ).aggregate(models.Sum('valeur'))['valeur__sum'] or 0

    def repartition_centre_total(self, centre_operationnel, centre_structure):
        return self.repartition_centre(centre_operationnel, centre_structure) + self.total_centre(centre_operationnel.id)

    def repartition_centre_pourcentage(self, centre_operationnel, centre_structure):
        return self.repartition_centre(centre_operationnel, centre_structure) / self.total_centre(centre_structure.id) * 100

    def total_general_direct(self):
        centres = Centre.list_operationnel()
        total = 0
        for centre_oper in centres:
            total += self.total_centre(centre_oper.id)
        return total

    def total_general_repartition(self, centre_structure):
        centres = Centre.list_operationnel()
        total = 0
        for centre_oper in centres:
            total += self.repartition_centre(centre_oper, centre_structure)
        return total

    def total_general(self, centre_structure):
        centres = Centre.list_operationnel()
        total = 0
        for centre_oper in centres:
            total += self.repartition_centre_total(centre_oper, centre_structure)
        return total

