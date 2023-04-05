from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models


class Journal(models.Model):
    icon = models.CharField(max_length=100, null=True, default='fas fa-question-circle')
    color = models.CharField(max_length=100, null=True, default='secondary')
    code = models.CharField(max_length=2, validators=[MinLengthValidator(2)], unique=True)
    nom = models.CharField(max_length=100)

    def __str__(self):
        return self.code + " " + self.nom

    # getters and setters
    def get_code(self):
        return self.code

    def set_code(self, code):
        if len(code) != 2:
            raise ValidationError("Le code doit être composé de 2 caractères")
        self.code = code

    def get_nom(self):
        return self.nom

    def set_nom(self, nom):
        if len(nom) == 0:
            raise ValidationError("Le nom ne peut être vide")
        if len(nom) > 100:
            raise ValidationError("Le nom ne peut pas dépasser 100 caractères")
        self.nom = nom

    def get_icon(self):
        return self.icon

    def set_icon(self, icon):
        if len(icon) == 0:
            raise ValidationError("L'icône ne peut être vide")
        if len(icon) > 100:
            raise ValidationError("L'icône ne peut pas dépasser 100 caractères")
        self.icon = icon

    def get_color(self):
        return self.color

    def set_color(self, color):
        if len(color) == 0:
            raise ValidationError("La couleur ne peut être vide")
        if len(color) > 100:
            raise ValidationError("La couleur ne peut pas dépasser 100 caractères")
        self.color = color

    @staticmethod
    def create(code, nom, icon=None, color=None):
        journal = Journal()
        journal.set_code(code)
        journal.set_nom(nom)
        if icon is not None:
            journal.set_icon(icon)
        if color is not None:
            journal.set_color(color)
        journal.save()
        return journal

    def update(self, code, nom, icon=None, color=None):
        self.set_code(code)
        self.set_nom(nom)
        if icon is not None:
            self.set_icon(icon)
        if color is not None:
            self.set_color(color)
        self.save()
        return self

    def remove(self):
        self.delete()
        return 0
