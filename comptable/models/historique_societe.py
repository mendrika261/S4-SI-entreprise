from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils import timezone

from . import StatusEntreprise, Devise


def validate_date_not_in_future(value):
    if value > timezone.now().date():
        raise ValidationError('La date de création ne peut pas être dans le futur')


def get_valid_scan_file_extension():
    return ['pdf', 'png', 'jpg', 'jpeg']


class HistoriqueSociete(models.Model):
    nom = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='upload/societe/')
    objectif = models.CharField(max_length=255)
    siege = models.CharField(max_length=100)
    status_entreprise = models.ForeignKey(StatusEntreprise, on_delete=models.CASCADE)
    date_creation = models.DateField(validators=[validate_date_not_in_future])
    nif = models.CharField(max_length=20)
    scan_nif = models.FileField(upload_to='upload/societe/',
                                validators=[FileExtensionValidator(get_valid_scan_file_extension())])
    stat = models.CharField(max_length=20)
    scan_stat = models.FileField(upload_to='upload/societe/',
                                 validators=[FileExtensionValidator(get_valid_scan_file_extension())])
    reg_commerce = models.CharField(max_length=20)
    scan_reg_commerce = models.FileField(upload_to='upload/societe/',
                                         validators=[FileExtensionValidator(get_valid_scan_file_extension())])
    devise_compte = models.ForeignKey(Devise, on_delete=models.CASCADE)
    date_information = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.nom

    @staticmethod
    def get_last_information():
        return HistoriqueSociete.objects.order_by('-date_information').first()
