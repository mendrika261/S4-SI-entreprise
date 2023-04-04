from django.core.exceptions import ValidationError
from django.core.validators import MinValueValidator
from django.db import models

from . import Devise


class DeviseEquivalente(models.Model):
    devise = models.ForeignKey(Devise, on_delete=models.CASCADE)
    devise_equivalente = models.ForeignKey(Devise, on_delete=models.CASCADE, related_name='devise_equivalente')
    taux = models.DecimalField(max_digits=10, decimal_places=2, validators=[MinValueValidator(0)])
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.devise.nom + ' - ' + self.devise_equivalente.nom

    class Meta:
        verbose_name = 'Devise Equivalente'
        verbose_name_plural = 'Devises Equivalente'

