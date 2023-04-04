from django.core.exceptions import ValidationError
from django.db import models

from . import CompteGeneral, CompteTiers, Devise, Piece


class EcritureJournal(models.Model):
    journal = models.ForeignKey('Journal', on_delete=models.CASCADE)
    date = models.DateField()
    piece = models.ForeignKey(Piece, on_delete=models.CASCADE)
    compte_general = models.ForeignKey(CompteGeneral, on_delete=models.CASCADE)
    compte_tiers = models.ForeignKey(CompteTiers, on_delete=models.CASCADE, null=True, default=None)
    intitule = models.CharField(max_length=100)
    devise = models.ForeignKey(Devise, on_delete=models.CASCADE)
    debit = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    credit = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)

    def __str__(self):
        return str(self.compte_general) + " - " + self.intitule

