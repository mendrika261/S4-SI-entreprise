from django.db import models


class Analyse(models.Model):
    centre = models.ForeignKey('Centre', on_delete=models.CASCADE)
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    pourcentage = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    valeur = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    quantite = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    fixe = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    variable = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    incorporable = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    non_incorporable = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    ecriture = models.ForeignKey('EcritureJournal', on_delete=models.CASCADE)

    def set_pourcentage(self, pourcentage):
        self.pourcentage = pourcentage

    def set_valeur(self, valeur):
        self.valeur = valeur

    def set_fixe(self, fixe):
        self.fixe = fixe

    def set_variable(self, variable):
        self.variable = variable

    def set_incorporable(self, incorporable):
        self.incorporable = incorporable

    def set_non_incorporable(self, non_incorporable):
        self.non_incorporable = non_incorporable

    def set_quantite(self, quantite):
        self.quantite = quantite
