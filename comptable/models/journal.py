from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models, IntegrityError


class Journal(models.Model):
    icon = models.CharField(max_length=100, null=True, default='fas fa-question-circle')
    color = models.CharField(max_length=100, null=True, default='secondary')
    code = models.CharField(max_length=2, validators=[MinLengthValidator(2)], unique=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return str(self.code).upper() + "-" + self.nom

    # Setters

    def set_code(self, code):
        if code != '' and code is not None and len(str(code)) != 2:
            raise ValidationError("Le code du journal doit être composé de 2 caractères")
        self.code = code

    def set_nom(self, nom):
        if nom == '' or nom is None:
            raise ValidationError("Le nom ne peut être vide")
        if len(str(nom)) > 100:
            raise ValidationError("Le nom ne peut pas dépasser 100 caractères")
        self.nom = nom

    def set_icon(self, icon):
        if icon == '' or icon is None:
            raise ValidationError("L'icône ne peut être vide")
        if len(str(icon)) > 100:
            raise ValidationError("L'icône ne peut pas dépasser 100 caractères")
        self.icon = icon

    def set_color(self, color):
        if color == '' or color is None:
            raise ValidationError("La couleur ne peut être vide")
        if len(str(color)) > 100:
            raise ValidationError("La couleur ne peut pas dépasser 100 caractères")
        self.color = color

    # Methods
    @staticmethod
    def create(code, nom, icon=None, color=None):
        journal = Journal()
        journal.set_code(code)
        journal.set_nom(nom)
        if icon is not None:
            journal.set_icon(icon)
        if color is not None:
            journal.set_color(color)
        try:
            journal.save()
        except IntegrityError:
            raise ValidationError("Le code du journal existe déjà")
        return journal

    def update(self, code, nom, icon=None, color=None):
        self.set_code(code)
        self.set_nom(nom)
        if icon is not None:
            self.set_icon(icon)
        if color is not None:
            self.set_color(color)
        try:
            self.save()
        except IntegrityError:
            raise ValidationError("Le code du journal existe déjà")
        return self

    def remove(self):
        self.delete()
        return 0
