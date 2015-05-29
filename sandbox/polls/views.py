#Modules 
from django.shortcuts import render
from django.http import HttpResponse


# Import le models pour pourvoir interoger la BD
from .models import Question

# module pour la version longue
##from django.template import RequestContext, loader

# module version courte de l'affichage avec template
from django.shortcuts import render

# Create your views here.
def index(request):
    latest_question_list = Question.objects.order_by('-pub_date')[:5]
    context = {'latest_question_list': latest_question_list}
    return render(request, 'polls/index.html', context)

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

def results(request, question_id):
    response = "You're looking at the results of question %s."
    return HttpResponse(response % question_id)

def vote(request, question_id):
    return HttpResponse("You're voting on question %s." % question_id)
