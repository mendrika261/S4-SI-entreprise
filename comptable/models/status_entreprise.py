from django.core.exceptions import ValidationError
from django.db import models, IntegrityError


class StatusEntreprise(models.Model):
    nom = models.CharField(max_length=50)
    sigle = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nom + ' (' + self.sigle + ')'

    # Setters
    def set_nom(self, nom):
        if nom == '' or nom is None:
            raise ValidationError("Le nom du status d'entreprise ne peut pas être vide")
        if len(str(nom)) >= 50:
            raise ValidationError("Le nom du status d'entreprise ne peut dépasser 50 caractères")
        self.nom = nom

    def set_sigle(self, sigle):
        if sigle == '' or sigle is None:
            raise ValidationError("Le sigle d'un status ne peut pas être vide")
        if len(str(sigle)) > 10:
            raise ValidationError("Le sigle d'un status ne peut pas dépasser 10 caractères")
        self.sigle = sigle

    # Methods
    @staticmethod
    def create(nom, sigle):
        status_entreprise = StatusEntreprise()
        status_entreprise.set_nom(nom)
        status_entreprise.set_sigle(sigle)
        try:
            status_entreprise.save()
        except IntegrityError:
            raise ValidationError("Le sigle '" + sigle + "' est déjà utilisé")
        return status_entreprise

    def update(self, nom, sigle):
        self.set_nom(nom)
        self.set_sigle(sigle)
        try:
            self.save()
        except IntegrityError:
            raise ValidationError("Le sigle '" + sigle + "' est déjà utilisé")
        return self

    def remove(self):
        self.delete()
        return 0
