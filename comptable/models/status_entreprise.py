from django.core.exceptions import ValidationError
from django.db import models


class StatusEntreprise(models.Model):
    nom = models.CharField(max_length=50)
    sigle = models.CharField(max_length=10, unique=True)

    def __str__(self):
        return self.nom + ' (' + self.sigle + ')'
