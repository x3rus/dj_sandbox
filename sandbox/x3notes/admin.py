from django.contrib import admin

# Register your models here.

from .models import Note , NoteAuthEmail

admin.site.register(Note)
admin.site.register(NoteAuthEmail)
