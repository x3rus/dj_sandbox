# Description :
#   Test units  for x3notes
#   
# 
# Auteur : Boutry Thomas <thomas.boutry@x3rus.com>
# Date de creation : 2015-06-30
# Licence : GPL v3.
###############################################################################


from django.test import TestCase



# Added modules
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User

# Ajout des models 
from django.db import models
from .models import Note, NoteAuthEmail

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

########################
# URL de l'utilisateur #
class UserViewTests(TestCase):
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

    # TODO Ajouter un test avec un usager authentifier 

    def test_user_view_for_bad_username(self):
        """
        Check user page without note
        """
        create_user("testuser",'password')
        response = self.client.get(reverse('x3notes:view_user',args=("testuserBAD",)))
        self.assertEqual(response.status_code, 404)


# TODO ajout des test pour l'ajout de note et l'edition
# TODO ajout des test pour l'edition de note 
# TODO ajout des test pour la suppression de note 
