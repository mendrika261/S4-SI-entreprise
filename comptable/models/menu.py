from django.core.exceptions import ValidationError
from django.db import models


class Menu (models.Model):
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=100, null=True, blank=True)
    url = models.CharField(max_length=100, null=True, blank=True)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='children', on_delete=models.CASCADE)
    order = models.IntegerField(default=0)

    def __str__(self):
        label = (self.parent.name.title() + ' >> ') if self.parent is not None else ''
        return str(self.order) + " - " + label + self.name

    class Meta:
        ordering = ['order']

    def clean_fields(self, exclude=None):
        if len(self.name) > 100:
            raise ValidationError("Le nom ne doit pas dépasser 100 caractères")
        if len(self.icon) > 100:
            raise ValidationError("L'icone ne doit pas dépasser 100 caractères")
        if len(self.url) > 100:
            raise ValidationError("L'url ne doit pas dépasser 100 caractères")
        if self.parent is not None and self.parent.parent is not None:
            raise ValidationError("Le menu ne peut pas avoir plus de 2 niveaux")
        self.name = self.name.upper()

    @staticmethod
    def get_menu():
        return Menu.objects.filter(parent=None).order_by('order')

    def sub_menu(self):
        return self.children.all().order_by('order')

    def have_sub_menu(self):
        return self.children.all().count() > 0
