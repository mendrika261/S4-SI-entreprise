from django.core.exceptions import ValidationError
from django.db import models


class CodeJournal(models.Model):
    code = models.CharField(max_length=2, unique=True)
    intitule = models.CharField(max_length=100)

    def __str__(self):
        return str(self.code) + ' - ' + str(self.intitule)

    class Meta:
        verbose_name = 'Code journal'
        verbose_name_plural = 'Codes journal'

    # Getters and setters
    def get_code(self):
        return self.code

    def set_code(self, code):
        if len(code) != 2:
            raise ValidationError('Le code doit avoir 2 caractères')
        self.code = str(code).upper()

    def get_intitule(self):
        return self.intitule

    def set_intitule(self, intitule):
        if len(intitule) < 3:
            raise ValidationError('L\'intitulé doit avoir au moins 3 caractères')
        if len(intitule) > 100:
            raise ValidationError('L\'intitulé doit avoir au plus 100 caractères')
        self.intitule = str(intitule).capitalize()

    # Methods
    @staticmethod
    def create(code, intitule):
        code_journal = CodeJournal()
        code_journal.set_code(code)
        code_journal.set_intitule(intitule)
        code_journal.save()
        return code_journal

    def update(self, code, intitule):
        self.set_code(code)
        self.set_intitule(intitule)
        self.save()
        return self

    def remove(self):
        self.delete()
        return 0
