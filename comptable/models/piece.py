from django.core.exceptions import ValidationError
from django.db import models, IntegrityError
from . import Journal


class Piece(models.Model):
    prefixe = models.ForeignKey(Journal, on_delete=models.CASCADE)
    numero = models.CharField(unique=True, max_length=50)
    fichier = models.FileField(null=True, default=None, blank=True, upload_to='pieces/')

    def __str__(self):
        return str(self.prefixe.code).upper() + "-" + str(self.numero).upper()

    # Setters
    def set_prefixe(self, prefixe_id):
        try:
            self.prefixe = Journal.objects.get(id=prefixe_id)
        except Exception:
            raise ValidationError("Le préfixe de la pièce n'existe pas")

    def set_numero(self, numero):
        if numero == '' or numero is None:
            raise ValidationError('Le numéro de la pièce ne peut pas être vide')
        if len(str(numero)) > 50:
            raise ValidationError('Le numéro de la pièce ne peut pas dépasser 50 caractères')
        self.numero = numero

    # Methods
    @staticmethod
    def create(prefixe, numero, fichier=None):
        piece = Piece()
        piece.set_numero(numero)
        piece.set_prefixe(prefixe)
        if fichier is not None:
            piece.fichier = fichier
        try:
            piece.save()
        except IntegrityError:
            raise ValidationError(f'La pièce {piece} existe déjà')
        return piece

    def update(self, prefixe, numero, fichier=None):
        self.set_prefixe(prefixe)
        self.set_numero(numero)
        if fichier is not None:
            self.fichier = fichier
        try:
            self.save()
        except IntegrityError:
            raise ValidationError(f'La pièce {self} existe déjà')
        return self

    def remove(self):
        self.delete()
        return 0
