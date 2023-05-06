from django.core.exceptions import ValidationError
from django.db import models, transaction, IntegrityError


class CompteGeneral(models.Model):
    code = models.CharField(max_length=5, unique=True)
    intitule = models.CharField(max_length=100)

    def __str__(self):
        return str(self.code) + ' - ' + self.intitule

    class Meta:
        verbose_name = 'Compte général'
        verbose_name_plural = 'Comptes généraux'

    # Setters
    def set_code(self, code):
        if code == '' or code is None:
            raise ValidationError('Le code ne peut pas être vide')
        if len(str(code)) != 5:
            raise ValidationError('Le code doit avoir 5 caractères')
        self.code = code

    def set_intitule(self, intitule):
        if intitule == '' or intitule is None:
            raise ValidationError("")
        if len(str(intitule)) > 100:
            raise ValidationError("")
        self.intitule = intitule

    # Methods
    @staticmethod
    def create(code, intitule):
        compte_general = CompteGeneral()
        compte_general.set_code(code)
        compte_general.set_intitule(intitule)
        compte_general.clean_fields()
        try:
            compte_general.save()
        except IntegrityError:
            raise ValidationError("Le code " + str(code) + " existe déjà")
        return compte_general

    def update(self, code, intitule):
        self.set_code(code)
        self.set_intitule(intitule)
        try:
            self.save()
        except IntegrityError:
            raise ValidationError("Le code " + str(code) + " existe déjà")
        return self

    def remove(self):
        self.delete()
        return 0

    @staticmethod
    @transaction.atomic
    def import_from_csv(file, with_header=True):
        import csv
        try:
            with open(file, 'r') as f:
                reader = csv.reader(f)
                if with_header:
                    next(reader)
                for row in reader:
                    try:
                        CompteGeneral.create(row[0], row[1])
                    except ValidationError as e:
                        raise ValidationError("Erreur lors de l'importation à la ligne " + str(row) + " : \n" + str(e))
        except FileNotFoundError:
            raise ValidationError("Le traitement du fichier a échoué! <br> Vérifier que le fichier est un .csv et "
                                  "l'ordre des colonnes")
        return 0
