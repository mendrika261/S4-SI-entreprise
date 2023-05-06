from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models, IntegrityError


class Devise(models.Model):
    code = models.CharField(max_length=3, unique=True, validators=[MinLengthValidator(3)])
    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.nom + ' (' + self.code + ')'

    class Meta:
        verbose_name = 'Devise'
        verbose_name_plural = 'Devises'

    # Setters

    def set_code(self, code):
        if code == "" and code is None:
            raise ValidationError("Vous devez taper un code ")
        if len(str(code)) != 3:
            raise ValidationError("Le code doit etre compose de 3 lettres")
        self.code = code

    def set_nom(self, nom):
        if nom == "" and nom is None:
            raise ValidationError("Vous devez taper un nom ")
        if len(str(nom)) > 50:
            raise ValidationError("Le nom ne doit pas dépasser 50 caracteres")
        self.nom = nom

    # Methods
    @staticmethod
    def create(code, nom):
        devise = Devise()
        devise.set_code(code)
        devise.set_nom(nom)
        try:
            devise.save()
        except IntegrityError:
            raise ValidationError("Cette devise existe deja")
        return devise

    def update(self, code, nom):
        self.set_code(code)
        self.set_nom(nom)
        try:
            self.save()
        except IntegrityError:
            raise ValidationError("Cette devise existe deja")
        return self

    def remove(self):
        self.delete()
        return 0
