from django.shortcuts import render, get_object_or_404


# Mise en place des racoursis de code 
from django.views import generic
from django.contrib.auth import authenticate, login
from django.http import HttpResponse, HttpResponseRedirect

# Models 
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .models import Note, NoteAuthEmail
from .forms import NoteForm, NoteEditForm


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
    # user2poll = User.objects.get(username=username)
    user2poll = get_object_or_404(User, username=username)
    public_notes = Note.objects.filter(ispublic=True).filter(owner=user2poll)
    private_notes = Note.objects.filter(ispublic=False).filter(owner=user2poll)
    context = {'public_notes': public_notes}
    return render(request, 'x3notes/view_user.html', {'username': username,
                                                     'public_notes': public_notes,
                                                     'private_notes': private_notes})

# ajout de l'obligation d'authentification
# @login_required
# def add_note(request,username):
    # TODO est-ce pertinent de valider que l'utilisateur dans l'URL est equivalent a l'utilisateur
    # authentifier... a analyser ... 
    # if not request.user.email.endswith('@example.com'):
    #    return redirect('/login/?next=%s' % request.path)
#    
    # Recuperation du user en argument  
#    p = get_object_or_404(User, username=username)
#    try:
#        selected_choice = p.choice_set.get(pk=request.POST['choice'])
# Username donne la string du nom je fais un recherche pour avoir l'object
#    user2poll = User.objects.get(username=username)
#    public_notes = Note.objects.filter(ispublic=True).filter(owner=user2poll)
#    context = {'public_notes': public_notes}
#    return render(request, 'x3notes/view_user.html', {'username': username, 'public_notes': public_notes})

@login_required
def edit_note(request,note_id):
    note = get_object_or_404(Note, pk=note_id)
    
    # TODO Ajouter la restriction si le demandeur est le owner
    # sinon redirection vers une page d'erreur .
    if note.owner.username != request.user.username:
        return render(request, 'x3notes/no_access.html')

     # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NoteEditForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            # TODO trouver une autre method pour l'assignation !!!
            note.title = form.cleaned_data['title']
            note.text = form.cleaned_data['text']
            note.ispublic = form.cleaned_data['ispublic']
            note.owner = request.user
            note.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/x3notes/'+ request.user.username)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NoteEditForm(instance=note)

    return render(request, 'editnote.html', {'form': form,
                                            'username': request.user.username,
                                            'note_id': note_id })
@login_required
def del_note(request,note_id):
    note = get_object_or_404(Note, pk=note_id)
    
    # TODO eventuellement mettre une confirmation de suppression 
    # TODO permettre la suppresion en masse de notes
    if note.owner.username == request.user.username:
        note_title = note.title
        note.delete()
        # return HttpResponseRedirect('/x3notes/'+ request.user.username)
        return render(request, 'delnote.html' , {'note_title': note_title,
                                                 'username': request.user.username})
    else:
        return render(request, 'x3notes/no_access.html')


@login_required
def add_note(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = NoteForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            a_new_note = Note()
            # TODO trouver une autre method pour l'assignation !!!
            a_new_note.title = form.cleaned_data['title']
            a_new_note.text = form.cleaned_data['text']
            a_new_note.ispublic = form.cleaned_data['ispublic']
            a_new_note.owner = request.user
            a_new_note.save()
            # redirect to a new URL:
            return HttpResponseRedirect('/x3notes/'+ request.user.username)

    # if a GET (or any other method) we'll create a blank form
    else:
        form = NoteForm()

    return render(request, 'addnote.html', {'form': form, 'username': request.user.username })


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

