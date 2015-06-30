from django.shortcuts import render


# Mise en place des racoursis de code 
#from django.views import generic
from django.http import HttpResponse


# Create your views here.
#class IndexView(generic.DetailView):
#    template_name = 'x3notes/index.html'

def index(request):
    return HttpResponse("It will show list of users")

