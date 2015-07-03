from django.shortcuts import render


# Mise en place des racoursis de code 
from django.views import generic
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

# Models 
from django.contrib.auth.models import User
from .models import Note, NoteAuthEmail


# Create your views here.
class IndexView(generic.ListView):
    template_name = 'x3notes/index.html'
    context_object_name = 'lst_users'

    def get_queryset(self):
        """Return list of users"""
        return User.objects.order_by('-username')
#        return Question.objects.filter( pub_date__lte=timezone.now()).order_by('-pub_date')[:5]

def profile_user(request):
    return render(request, 'x3notes/profile.html')

def view_user(request,username):
    # Username donne la string du nom je fais un recherche pour avoir l'object
    # telle que contenu dans la BD
    user2poll = User.objects.get(username=username)
    public_notes = Note.objects.filter(ispublic=True).filter(owner=user2poll)
    context = {'public_notes': public_notes}
    return render(request, 'x3notes/view_user.html', {'username': username, 'public_notes': public_notes})


######################################################################################################

#################
#### Obsolet ####
#################
# mais je garde comme source d'apprentissage
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

