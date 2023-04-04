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
