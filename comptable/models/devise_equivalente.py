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

    # Setters
    def set_date(self, date):
        self.date = date

    def set_taux(self, taux):
        if len(str(taux)) == 0:
            raise ValidationError('Le taux ne peut pas être vide')
        try:
            taux = float(taux)
        except ValueError:
            raise ValidationError('Le taux doit être un nombre')
        if taux < 0:
            raise ValidationError('Le taux ne peut pas être négatif')

        self.taux = taux

    def set_devise(self, devise_id):
        try:
            self.devise = Devise.objects.get(id=devise_id)
        except Exception:
            raise ValidationError("La devise n'existe pas")

    def set_devise_equivalente(self, devise_equivalente_id):
        try:
            self.devise_equivalente = Devise.objects.get(id=devise_equivalente_id)
        except Exception:
            raise ValidationError("La devise équivalente n'existe pas")
        finally:
            if self.devise and self.devise_equivalente == self.devise:
                raise ValidationError("La devise équivalente ne peut pas être la même que la devise")

    # Methods
    @staticmethod
    def create(devise_id, devise_equivalente_id, taux):
        equivalence = DeviseEquivalente()
        equivalence.set_devise(devise_id)
        equivalence.set_devise_equivalente(devise_equivalente_id)
        equivalence.set_taux(taux)
        equivalence.save()
        return equivalence

    def update(self, devise_id, devise_equivalente_id, taux):
        self.set_devise(devise_id)
        self.set_devise_equivalente(devise_equivalente_id)
        self.set_taux(taux)
        self.save()
        return self

    def remove(self):
        self.delete()
        return 0
