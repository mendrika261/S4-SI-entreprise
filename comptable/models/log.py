from django.db import models
from django.utils.timezone import now


class Log(models.Model):
    title = models.CharField(max_length=100)
    icon = models.CharField(max_length=100)
    content = models.CharField(max_length=1000, blank=True)
    color = models.CharField(max_length=50)
    date = models.DateTimeField()

    def __str__(self):
        return str(self.date) + " - " + str(self.title)

    @staticmethod
    def create(title, content='', icon='fas fa-info', color='secondary', date=now()):
        log = Log()
        log.title = title
        log.icon = icon
        log.content = content
        log.color = color
        log.date = date
        log.save()
        return log

