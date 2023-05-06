from django.core.exceptions import ValidationError
from django.db import models, IntegrityError

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

    # Setters

    def set_code(self, code):
        if code == '' and code is None:
            raise ValidationError('Le code ne peut pas être vide')
        if len(str(code)) > 13:
            raise ValidationError('Le code ne peut pas dépasser 13 caractères')
        self.code = code

    def set_intitule(self, intitule):
        if intitule == '' and intitule is None:
            raise ValidationError('L\'intitulé ne peut pas être vide')
        if len(str(intitule)) > 100:
            raise ValidationError('L\'intitulé ne peut pas dépasser 100 caractères')
        self.intitule = intitule

    def set_compte_general(self, compte_general_id):
        try:
            self.compte_general = CompteGeneral.objects.get(id=compte_general_id)
        except Exception:
            raise ValidationError('Le compte général n\'existe pas')

    # Methods
    @staticmethod
    def create(compte_general_id, code, intitule):
        compte_tiers = CompteTiers()
        compte_tiers.compte_general = CompteGeneral.objects.get(id=compte_general_id)
        compte_tiers.set_code(code)
        compte_tiers.set_intitule(intitule)
        try:
            compte_tiers.save()
        except IntegrityError:
            raise ValidationError('Le compte tiers existe déjà')
        return compte_tiers

    def update(self, compte_general_id, code, intitule):
        self.compte_general = CompteGeneral.objects.get(id=compte_general_id)
        self.set_code(code)
        self.set_intitule(intitule)
        try:
            self.save()
        except IntegrityError:
            raise ValidationError('Le compte tiers existe déjà')
        return self

    def remove(self):
        self.delete()
        return 0
