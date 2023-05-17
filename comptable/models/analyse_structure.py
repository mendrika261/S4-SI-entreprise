from django.db import models


class AnalyseStructure(models.Model):
    ecriture = models.ForeignKey('EcritureJournal', on_delete=models.CASCADE)
    produit = models.ForeignKey('Produit', on_delete=models.CASCADE)
    centre_structure = models.ForeignKey('Centre', on_delete=models.CASCADE, related_name='centre_structure')
    centre_operationnel = models.ForeignKey('Centre', on_delete=models.CASCADE, related_name='centre_operationnel')
    pourcentage = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
    valeur = models.DecimalField(max_digits=20, decimal_places=2, default=0, blank=True)
