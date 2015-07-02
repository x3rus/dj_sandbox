from django.shortcuts import render


# Mise en place des racoursis de code 
from django.views import generic
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth.models import User

# Create your views here.
class IndexView(generic.ListView):
    template_name = 'x3notes/index.html'
    context_object_name = 'lst_users'

    def get_queryset(self):
        """Return list of users"""
        return User.objects.order_by('-username')
#        return Question.objects.filter( pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

def auth_user(request):
    try:
        username = request.POST['username']
        password = request.POST['password']
    except :
        # Redisplay the question voting form.
        return render(request, 'x3notes/auth.html', {

            })
    else:
        user = authenticate(username=username, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                # Redirect to a success page.
                return HttpResponseRedirect('http://x3rus.com/go')
            else:
                return HttpResponseRedirect('http://google.com/go')
        else:
                # Return an 'invalid login' error message.
                return HttpResponseRedirect('http://x3rus.com/error')

#def index(request):
#    return HttpResponse("It will show list of users")

def profile_user(request):
    return render(request, 'x3notes/profile.html')
