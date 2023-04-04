from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator
from django.db import models


class Devise(models.Model):
    code = models.CharField(max_length=3, unique=True, validators=[MinLengthValidator(3)])
    nom = models.CharField(max_length=50)

    def __str__(self):
        return self.nom + ' (' + self.code + ')'

    class Meta:
        verbose_name = 'Devise'
        verbose_name_plural = 'Devises'
