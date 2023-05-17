from django.contrib.humanize.templatetags.humanize import intcomma
from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from django.utils.timezone import now


class Centre(models.Model):
    CATEGORY = (
        ('structure', 'Structure'),
        ('opérationnel', 'Opérationnel'),
    )
    nom = models.CharField(max_length=100, unique=True)
    categorie = models.CharField(max_length=50, choices=CATEGORY)

    def __str__(self):
        return self.nom

    def set_nom(self, nom):
        if nom == '' or None:
            raise ValidationError('Le nom du centre ne peut pas être vide')
        try:
            self.nom = str(nom).capitalize()
        except IntegrityError:
            raise ValidationError('Le nom du centre doit être unique')

    def set_categorie(self, categorie):
        if type == '' or None:
            raise ValidationError('Le type du centre ne peut pas être vide')
        self.categorie = categorie

    @staticmethod
    def create(nom, categorie):
        centre = Centre()
        centre.set_nom(nom)
        centre.set_categorie(categorie)
        centre.save()
        return centre

    def update(self, nom, categorie):
        self.set_nom(nom)
        self.set_categorie(categorie)
        self.save()
        return self

    def remove(self):
        self.delete()
        return 0

    def get_total(self, date=now()):
        from comptable.models import Analyse
        return Analyse.objects.filter(
            centre_id=self.id,
            ecriture__date__lte=date
        ).aggregate(models.Sum('valeur'))['valeur__sum'] or 0

    def charge_produit(self, id_produit, date=now()):
        from comptable.models import Analyse
        return Analyse.objects.filter(
            centre_id=self.id,
            produit_id=id_produit,
            ecriture__date__lte=date,
        ).aggregate(models.Sum('valeur'))['valeur__sum'] or 0

    def charge_produit_pourcentage(self, id_produit, date=now()):
        total = self.get_total(date) or 1
        temp = self.charge_produit(id_produit, date)
        return temp / total * 100

    def charge_produit_fixe(self, id_produit, date=now()):
        """from comptable.models import Analyse
        comptes = Analyse.objects.filter(
            centre_id=self.id,
            produit_id=id_produit,
            ecriture__date__lte=date,
        )
        sum_value = 0
        reference = self.charge_produit(id_produit, date)
        total = self.get_total(date)
        charge_produit_p = self.charge_produit_pourcentage(id_produit, date)
        for compte in comptes:
            sum_value += float(total) * (float(compte.fixe) / 100) * (float(charge_produit_p) / 100)
        return sum_value"""
        from comptable.models import Produit
        produit = Produit.objects.get(id=id_produit)
        return produit.total_fixe(self.id, date)

    def charge_produit_variable(self, id_produit, date=now()):
        """from comptable.models import Analyse
        comptes = Analyse.objects.filter(
            centre_id=self.id,
            produit_id=id_produit,
            ecriture__date__lte=date,
        )
        sum_value = 0
        reference = self.charge_produit(id_produit, date)
        total = self.get_total(date)
        charge_produit_p = self.charge_produit_pourcentage(id_produit, date)
        for compte in comptes:
            sum_value += float(total) * float(compte.variable) / 100 * float(charge_produit_p) / 100
        return sum_value"""
        from comptable.models import Produit
        produit = Produit.objects.get(id=id_produit)
        return produit.total_variable(self.id, date)

    def charge_produit_incorporable(self, id_produit, date=now()):
        from comptable.models import Analyse
        comptes = Analyse.objects.filter(
            centre_id=self.id,
            produit_id=id_produit,
            ecriture__date__lte=date,
        )
        sum_value = 0
        total = self.get_total(date)
        charge_produit_p = self.charge_produit_pourcentage(id_produit, date)
        for compte in comptes:
            sum_value += float(compte.valeur) * float(compte.incorporable) / 100 * float(charge_produit_p) / 100
        return sum_value

    def charge_produit_non_incorporable(self, id_produit, date=now()):
        from comptable.models import Analyse
        comptes = Analyse.objects.filter(
            centre_id=self.id,
            produit_id=id_produit,
            ecriture__date__lte=date,
        )
        sum_value = 0
        total = self.get_total(date)
        charge_produit_p = self.charge_produit_pourcentage(id_produit, date)
        for compte in comptes:
            sum_value += float(compte.valeur) * float(compte.non_incorporable) / 100 * float(charge_produit_p) / 100
        return sum_value

    def total_charge_fixe(self):
        sum_v = 0
        from comptable.models import Produit
        produits = Produit.objects.all()
        for c in produits:
            sum_v += self.charge_produit_fixe(c.id)
        return intcomma(round(sum_v, 2))

    def total_charge_variable(self):
        sum_v = 0
        from comptable.models import Produit
        produits = Produit.objects.all()
        for c in produits:
            sum_v += self.charge_produit_variable(c.id)
        return intcomma(round(sum_v, 2))

    def total_charge_incorporable(self):
        sum_v = 0
        from comptable.models import Produit
        produits = Produit.objects.all()
        for c in produits:
            sum_v += self.charge_produit_incorporable(c.id)
        return intcomma(round(sum_v, 2))

    def total_charge_non_incorporable(self):
        sum_v = 0
        from comptable.models import Produit
        produits = Produit.objects.all()
        for c in produits:
            sum_v += self.charge_produit_non_incorporable(c.id)
        return intcomma(round(sum_v, 2))

    @staticmethod
    def list_operationnel():
        return Centre.objects.filter(categorie='opérationnel')

    @staticmethod
    def list_structure():
        return Centre.objects.filter(categorie='structure')
