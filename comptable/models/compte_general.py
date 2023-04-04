from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models


class CompteGeneral(models.Model):
    code = models.CharField(max_length=5, unique=True)
    intitule = models.CharField(max_length=100)

    def __str__(self):
        return str(self.code) + ' - ' + self.intitule

    class Meta:
        verbose_name = 'Compte général'
        verbose_name_plural = 'Comptes généraux'

    # Getters and setters
    def get_code(self):
        return self.code

    def set_code(self, code):
        if len(code) != 5:
            raise ValidationError('Le code doit avoir 5 caractères')
        self.code = code

    def get_intitule(self):
        return self.intitule

    def set_intitule(self, intitule):
        if intitule == '':
            raise ValidationError("")
        if len(intitule) > 100:
            raise ValidationError("")
        self.intitule = intitule

    # methods
    @staticmethod
    def create(code, intitule):
        compte_general = CompteGeneral()
        compte_general.set_code(code)
        compte_general.set_intitule(intitule)
        compte_general.save()
        return compte_general

    def update(self, code, intitule):
        self.set_code(code)
        self.set_intitule(intitule)
        self.save()
        return self

    def remove(self):
        self.delete()
        return 0
