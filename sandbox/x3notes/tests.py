# Description :
#   Test units  for x3notes
#   
# 
# Auteur : Boutry Thomas <thomas.boutry@x3rus.com>
# Date de creation : 2015-06-30
# Licence : GPL v3.
###############################################################################


from django.test import TestCase, RequestFactory



# Added modules
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.http import Http404, HttpResponse


# Ajout des models 
from django.db import models

# local includes 
from .models import Note, NoteAuthEmail
from .views import view_user, add_note, edit_note , del_note

# Create your tests here.


##################
### VIEW tests ###
##################

def create_user(username,password):
        u = User.objects.create_user(username, username+"x3rus.com", password)
        u.save()
        return u

def create_note(owner,title,content,ispublic):
        a_note = Note.objects.create(title=title,text=content,ispublic=ispublic, owner=owner)
        a_note.save()
        return a_note

#########
# Index #
class IndexViewTests(TestCase):
    def test_index_view_basic(self):
        """
        Check the index page simple
        """
        response = self.client.get(reverse('x3notes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Listes Users availables")

    def test_index_with_users(self):
        """
        Create 2 users and check the are listed
        """
        create_user("user1",'password')
        create_user("user2",'password')
        response = self.client.get(reverse('x3notes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "user1")
        self.assertContains(response, "user2")

    def test_user_view_for_bad_username(self):
        """
        Check user page without note
        """
        create_user("testuser",'password')
        response = self.client.get(reverse('x3notes:view_user',args=("testuserBAD",)))
        self.assertEqual(response.status_code, 404)


########################
# URL de l'utilisateur #
class TestAnonymousUser(TestCase):
    def test_user_view_anonyme_without_note(self):
        """
        Check user page without note
        """
        create_user("testuser",'password')
        response = self.client.get(reverse('x3notes:view_user',args=("testuser",)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "testuser's public notes")

    def test_user_view_anonyme_with_notes(self):
        """
        Check user page with note
        """
        the_user = create_user("Auser",'password')
        create_note(the_user,"Le Titre de note","Contenu de la note",True)
        create_note(the_user,"Un deuxime Titre de note","si ca mache pour 1 pk pas 2 ",True)
        response = self.client.get(reverse('x3notes:view_user',args=("Auser",)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Auser's public notes")
        self.assertContains(response, "Le Titre")
        self.assertContains(response, "pour 1 pk pas 2")
 
    def test_user_view_anonyme_with_pub_and_priv_notes(self):
        """
        Check user page with note public and private ,
        L'utilisateur n'etant pas identifier les messages priver
        ne sont pas lisible
        """
        the_user = create_user("Auser",'password')
        create_note(the_user,"Le Titre de note la note public","Contenu pour tous",True)
        create_note(the_user,"Une message priver","juste pour moi ",False)
        response = self.client.get(reverse('x3notes:view_user',args=("Auser",)))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contenu pour tous")
        self.assertNotContains(response, "juste pour moi")

    def test_user_view_anonyme_add_note(self):
        """
        Try to add a note in anonymous mode
        get a redirection to the login page
        """
        response = self.client.get(reverse('x3notes:add_note'))
        self.assertEqual(response.status_code, 302)

    def test_user_view_anonyme_edit_note(self):
        """
        Try to edit a note in anonymous mode
        get a redirection to the login page
        """
        response = self.client.get(reverse('x3notes:edit_note', args=("23",)))
        self.assertEqual(response.status_code, 302)

    def test_user_view_anonyme_del_note(self):
        """
        Try to edit a note in anonymous mode
        get a redirection to the login page
        """
        response = self.client.get(reverse('x3notes:del_note', args=("23",)))
        self.assertEqual(response.status_code, 302)




class TestAuthUser(TestCase):
    """
        a bunch of test with authentication required.
    """ 
    def setUp(self):
        # Every test needs access to the request factory.
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
                            username='aAuthUser', email='aAuthUser@example.com', password='top_secret')
        self.user2 = User.objects.create_user(
                            username='aSecondUser', email='aSecondUser@example.com', password='top_secret')

        # Creation de note pour aAuthUser
        create_note(self.user,"Une message priver","juste pour moi ",False) 
        create_note(self.user,"Le Titre de note la note public","Contenu pour tous",True)
        # Creation de note pour aSecondUser
        create_note(self.user2,"private message ","a moi pour moi",False)
        create_note(self.user2,"le publique est cool ","Lisez moi ", True)

    def test_user_view_auth_with_pub_and_priv_notes(self):
        """
        Establish a connection with user = AauthUser and request to view
        his owne notes , user should see public AND private notes
        """
        # Create an instance of a GET request.
        request = self.factory.get(reverse('x3notes:view_user',args=("AuserAuth",)))
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Request view x3notes/AuserAuth with authenticate user AuserAuth
        response = view_user(request, self.user.username)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contenu pour tous")
        self.assertContains(response, "juste pour moi")

    def test_user_view_auth_with_pub_and_priv_notes_for_other_user(self):
        """
        Establish a connection with user2 = aSecondUser and request to view
        not for user AuserAuth, the user should see public not but not private ones
        """
        # Create an instance of a GET request.
        request = self.factory.get(reverse('x3notes:view_user',args=("AuserAuth",)))
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user2

        # Request view x3notes/AuserAuth with authenticate user aSecondUser
        response = view_user(request, self.user.username)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Contenu pour tous")
 
    def test_user_addnote_auth_user(self):
        """
        User authenticate and add a note , be sure de form is there
        """
        # Create an instance of a GET request.
        request = self.factory.get(reverse('x3notes:add_note'))
        # Recall that middleware are not supported. You can simulate a
        # logged-in user by setting request.user manually.
        request.user = self.user

        # Request view x3notes/AuserAuth with authenticate user aSecondUser
        response = add_note(request)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form action=")


    def test_user_editnote_owne_by_other_user(self):
        """
        User authenticate and try to edit a note from a other user
        """
        # Create an instance of a GET request. edit_note 3 , note owne by
        # aSecondUser
        request = self.factory.get(reverse('x3notes:edit_note', args=("3",)))
        # Authentification avec aAuthUser
        request.user = self.user

        # Request view x3notes/AuserAuth with authenticate user aSecondUser
        response = edit_note(request,3)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No access")

    def test_user_editnote_owne_by_user(self):
        """
        User authenticate and try to edit a note from a other user
        """
        # Create an instance of a GET request. edit_note 3 , note owne by
        # aSecondUser
        request = self.factory.get(reverse('x3notes:edit_note', args=("1",)))
        # Authentification avec aAuthUser
        request.user = self.user

        # Request view x3notes/AuserAuth with authenticate user aSecondUser
        response = edit_note(request,1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "form action=")

    def test_user_editnote_dont_exit(self):
        """
        User authenticate and try to edit a note from a other user
        """
        # Create an instance of a GET request. edit_note 3 , note owne by
        # aSecondUser
        request = self.factory.get(reverse('x3notes:edit_note', args=("100",)))
        # Authentification avec aAuthUser
        request.user = self.user

        self.assertRaises(Http404, edit_note, request, "100")


    def test_user_delnote_owne_by_other_user(self):
        """
        User authenticate and try to delete a note from a other user
        """
        # Create an instance of a GET request. del_note 3 , note owne by
        # aSecondUser
        request = self.factory.get(reverse('x3notes:del_note', args=("3",)))
        # Authentification avec aAuthUser
        request.user = self.user

        # Request view x3notes/AuserAuth with authenticate user aSecondUser
        response = del_note(request,3)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No access")

 

    def test_user_delnote_owne_by_user(self):
        """
        User authenticate and try to delete a note from a other user
        """
        # Create an instance of a GET request. del_note 3 , note owne by
        # aSecondUser
        request = self.factory.get(reverse('x3notes:del_note', args=("1",)))
        # Authentification avec aAuthUser
        request.user = self.user

        # Request view x3notes/AuserAuth with authenticate user aSecondUser
        response = del_note(request,1)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Note deleted")

    def test_user_delnote_dont_exit(self):
        """
        User authenticate and try to delete a note from a other user
        """
        # Create an instance of a GET request. del_note 3 , note owne by
        # aSecondUser
        request = self.factory.get(reverse('x3notes:del_note', args=("100",)))
        # Authentification avec aAuthUser
        request.user = self.user

        self.assertRaises(Http404, del_note, request, "100")






        

# TODO ajout des test pour l'ajout de note et l'edition
# TODO ajout des test pour l'edition de note 
# TODO ajout des test pour la suppression de note 
