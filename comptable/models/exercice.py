from django.core.exceptions import ValidationError
from django.db import models
from django.urls import reverse
from django.utils.timezone import now


class Exercice(models.Model):
    debut = models.DateField()
    fin = models.DateField()

    def __str__(self):
        return str(self.debut) + " à " + str(self.fin)

    # Setters
    def set_debut(self, debut):
        if debut == "" or debut is None:
            raise ValidationError("Vous devez taper une date de début")
        try:
            self.debut = debut
        except Exception:
            raise ValidationError("La forme de la date de début n'est pas valide")

    def set_fin(self, fin):
        if fin == "" or fin is None:
            raise ValidationError("Vous devez taper une date de fin ")
        if self.debut >= fin:
            raise ValidationError("La date de fin doit etre superieur a la date de debut")
        try:
            self.fin = fin
        except Exception:
            raise ValidationError("La forme de la date de fin n'est pas valide")

    # Methods
    @staticmethod
    def create(debut, fin):
        exercice = Exercice()
        exercice.set_debut(debut)
        exercice.set_fin(fin)
        exercice.save()
        return exercice

    def update(self, debut, fin):
        self.set_debut(debut)
        self.set_fin(fin)
        self.save()
        return self

    def remove(self):
        self.delete()
        return 0

    @staticmethod
    def get_current():
        obj = Exercice.objects.filter(debut__lte=now(), fin__gte=now()).first()
        if obj is None:
            raise ValidationError("Vous devez d'abord créer un exercice "
                                  "<a href='" + reverse('create_exercice') + "' class='text-bold'> Cliquer ici</a>")
        return obj
