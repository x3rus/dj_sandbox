from django.contrib import admin

# Register your models here.

from .models import Question, Choice


# Permet l'ajout de Reponse lors de la creation de question
# Stackedline et TabularInline dont 2 maniere d'afficher les reponses.
#class ChoiceInline(admin.StackedInline):
class ChoiceInline(admin.TabularInline):
    model = Choice
    extra = 3

class QuestionAdmin(admin.ModelAdmin):
    fieldsets = [
        (None,               {'fields': ['question_text']}),
        ('Date information', {'fields': ['pub_date'], 'classes': ['collapse']}),
    ]
    # Ajout de la liste des choix possibles 
    inlines = [ChoiceInline]

    # amelioration des champs visible lors du listing
    list_display = ('question_text', 'pub_date', 'was_published_recently')

    # Ajout d'un champ de recherche
    search_fields = ['question_text']

admin.site.register(Question, QuestionAdmin)
admin.site.register(Choice)
