from django.core.exceptions import ValidationError
from django.core.validators import FileExtensionValidator
from django.db import models
from django.utils.timezone import now

from . import StatusEntreprise, Devise


def validate_date_not_in_future(value):
    if value > now().date():
        raise ValidationError('La date de création ne peut pas être dans le futur')


def get_valid_scan_file_extension():
    return ['pdf', 'png', 'jpg', 'jpeg']


class HistoriqueSociete(models.Model):
    nom = models.CharField(max_length=100)
    logo = models.ImageField(upload_to='societe/logo/')
    objectif = models.CharField(max_length=255)
    siege = models.CharField(max_length=100)
    status_entreprise = models.ForeignKey(StatusEntreprise, on_delete=models.CASCADE)
    date_creation = models.DateField(validators=[validate_date_not_in_future])
    nif = models.CharField(max_length=20)
    scan_nif = models.FileField(upload_to='societe/scan_nif/',
                                validators=[FileExtensionValidator(get_valid_scan_file_extension())])
    stat = models.CharField(max_length=20)
    scan_stat = models.FileField(upload_to='societe/scan_stat/',
                                 validators=[FileExtensionValidator(get_valid_scan_file_extension())])
    reg_commerce = models.CharField(max_length=20)
    scan_reg_commerce = models.FileField(upload_to='societe/scan_reg_commerce/',
                                         validators=[FileExtensionValidator(get_valid_scan_file_extension())])
    devise_compte = models.ForeignKey(Devise, on_delete=models.CASCADE)
    date_information = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.nom

    @staticmethod
    def get_last_information():
        return HistoriqueSociete.objects.order_by('-date_information').first()

    def set_status_entreprise(self, status_entreprise_id):
        try:
            self.status_entreprise = StatusEntreprise.objects.get(id=status_entreprise_id)
        except Exception:
            raise ValidationError("Le status d'entreprise n'existe pas")

    def set_date_creation(self, date_creation):
        try:
            self.date_creation = date_creation
        except Exception:
            raise ValidationError("Le format de la date n'est pas valide")

    def set_devise_compte(self, devise_compte_id):
        try:
            self.devise_compte = Devise.objects.get(id=devise_compte_id)
        except Exception:
            raise ValidationError("Le devise de compte n'existe pas")

    @staticmethod
    def create_wt_file(nom, objectif, siege, status_entreprise_id, nif, stat, reg_commerce, devise_compte_id):
        historique_societe = HistoriqueSociete.get_last_information()

        new_historique_societe = HistoriqueSociete()
        new_historique_societe.id = None
        new_historique_societe.nom = str(nom).strip()
        new_historique_societe.objectif = str(objectif).strip()
        new_historique_societe.siege = str(siege).strip()
        new_historique_societe.set_status_entreprise(status_entreprise_id)
        new_historique_societe.date_creation = historique_societe.date_creation
        new_historique_societe.nif = nif
        new_historique_societe.stat = stat
        new_historique_societe.reg_commerce = reg_commerce
        new_historique_societe.set_devise_compte(devise_compte_id)
        new_historique_societe.date_information = now()
        new_historique_societe.logo = historique_societe.logo
        new_historique_societe.scan_nif = historique_societe.scan_nif
        new_historique_societe.scan_stat = historique_societe.scan_stat
        new_historique_societe.scan_reg_commerce = historique_societe.reg_commerce

        content = HistoriqueSociete.build_difference(new_historique_societe, historique_societe)
        if content == '':
            raise ValidationError('Aucune modification n\'a été effectuée')
        new_historique_societe.save()

        from comptable.models import Log
        Log.create("Modification d'information", content, "fas fa-edit", "info")

        return historique_societe

    @staticmethod
    def import_file(type_file, file):
        new_historique = HistoriqueSociete.get_last_information()
        if type_file == '1':
            nom = 'logo'
            new_historique.logo = file
            new_historique.save()
            content = "<img src='" + new_historique.logo.url + "' width=150 alt=' Fichier téléchargeable' />"
            content += "<br><a class='btn btn-success' href='" + new_historique.logo.url + \
                       "'>Télécharger le fichier</a>"
        elif type_file == '2':
            nom = 'scan nif'
            new_historique.scan_nif = file
            new_historique.save()
            content = "<img src='" + new_historique.scan_nif.url + "' width=150 alt=' Fichier " \
                                                                             "téléchargeable' />"
            content += "<br><a class='btn btn-success' href='" + new_historique.scan_nif.url + \
                       "'>Télécharger le fichier</a>"
        elif type_file == '3':
            nom = 'scan stat'
            new_historique.scan_stat = file
            new_historique.save()
            content = "<img src='" + new_historique.scan_stat.url + "' width=150 alt=' Fichier " \
                                                                              "téléchargeable' />"
            content += "<br><a class='btn btn-success' href='" + new_historique.scan_stat.url + \
                       "'>Télécharger le fichier</a>"
        elif type_file == '4':
            nom = 'scan registre de commerce'
            new_historique.scan_reg_commerce = file
            new_historique.save()
            content = "<img src='" + new_historique.scan_reg_commerce.url + "' width=150 alt=' Fichier " \
                                                                                      "téléchargeable' />"
            content += "<br><a class='btn btn-success' href='" + new_historique.scan_reg_commerce.url + \
                       "'>Télécharger le fichier</a>"
        else:
            raise ValidationError('Vous ne pouvez pas importer ce type de fichier!')
        new_historique.save()
        from comptable.models import Log
        Log.create('Changement de ' + nom, content, 'fas fa-file-import', 'info')

    @staticmethod
    def build_difference(historique_societe, last_historique_societe):
        difference = ""
        if historique_societe.nom != last_historique_societe.nom:
            difference += "<strong>Nom: </strong>" + historique_societe.nom + "<br>"
        if historique_societe.objectif != last_historique_societe.objectif:
            difference += "<strong>Objectif: </strong>" + historique_societe.objectif + "<br>"
        if historique_societe.siege != last_historique_societe.siege:
            difference += "<strong>Siège: </strong>" + historique_societe.siege + "<br>"
        if historique_societe.status_entreprise != last_historique_societe.status_entreprise:
            difference += "<strong>Status entreprise: </strong>" + historique_societe.status_entreprise.nom + "<br>"
        if historique_societe.date_creation != last_historique_societe.date_creation:
            difference += "<strong>Date création: </strong>" + str(historique_societe.date_creation) + "<br>"
        if historique_societe.nif != last_historique_societe.nif:
            difference += "<strong>NIF: </strong>" + historique_societe.nif + "<br>"
        if historique_societe.stat != last_historique_societe.stat:
            difference += "<strong>STAT: </strong>" + historique_societe.stat + "<br>"
        if historique_societe.reg_commerce != last_historique_societe.reg_commerce:
            difference += "<strong>Registre commerce: </strong>" + historique_societe.reg_commerce + "<br>"
        if historique_societe.devise_compte != last_historique_societe.devise_compte:
            difference += "<strong>Devise compte: </strong>" + historique_societe.devise_compte.nom + "<br>"

        return difference
