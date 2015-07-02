from django.db import models

# Mes modules
from django.contrib.auth.models import User

# Create your models here.

class Note(models.Model):
    # TODO : Voir pour les autre type disponible ... 
    # https://docs.djangoproject.com/en/1.8/ref/models/fields/
    title = models.CharField(max_length=255)
    text = models.CharField(max_length=255)
    owner = models.ForeignKey(User)
    ispublic = models.BooleanField(True)

    def __str__(self):
        return  '='.join([
            self.text,
            self.owner,
        ])

class NoteAuthEmail(models.Model):
    noteid = models.ForeignKey(Note)
    emailAuth = models.EmailField()


