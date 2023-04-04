from django.core.exceptions import ValidationError
from django.db import models

from . import CompteGeneral


class CompteTiers(models.Model):
    compte_general = models.ForeignKey(CompteGeneral, on_delete=models.CASCADE)
    code = models.CharField(max_length=13, unique=True)
    intitule = models.CharField(max_length=100)

    def __str__(self):
        return str(self.code) + ' - ' + self.intitule

    class Meta:
        verbose_name = 'Compte tiers'
        verbose_name_plural = 'Comptes tiers'

    # getters and setters
    def get_code(self):
        return self.code

    def set_code(self, code):
        if len(code) == 0:
            raise ValidationError('Le code ne peut pas être vide')
        if len(code) > 13:
            raise ValidationError('Le code ne peut pas dépasser 13 caractères')
        self.code = code

    def get_intitule(self):
        return self.intitule

    def set_intitule(self, intitule):
        if len(intitule) == 0:
            raise ValidationError('L\'intitulé ne peut pas être vide')
        if len(intitule) > 100:
            raise ValidationError('L\'intitulé ne peut pas dépasser 100 caractères')
        self.intitule = intitule

        # methods
    @staticmethod
    def create(compte_general_id, code, intitule):
        compte_tiers = CompteTiers()
        compte_tiers.compte_general = CompteGeneral.objects.get(id=compte_general_id)
        compte_tiers.set_code(code)
        compte_tiers.set_intitule(intitule)
        compte_tiers.save()
        return compte_tiers

    def update(self, compte_general_id, code, intitule):
        self.compte_general = CompteGeneral.objects.get(id=compte_general_id)
        self.set_code(code)
        self.set_intitule(intitule)
        self.save()
        return self

    def remove(self):
        self.delete()
        return 0
