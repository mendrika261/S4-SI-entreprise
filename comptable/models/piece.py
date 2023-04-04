from django.core.exceptions import ValidationError
from django.db import models

from . import CodeJournal


class Piece(models.Model):
    prefixe = models.ForeignKey(CodeJournal, on_delete=models.CASCADE)
    numero = models.CharField(unique=True, max_length=50)
    fichier = models.FileField(null=True, default=None, blank=True, upload_to='pieces/')

    def __str__(self):
        return self.prefixe.code + " " + self.numero
