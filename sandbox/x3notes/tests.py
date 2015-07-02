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
# Create your tests here.


##################
### VIEW tests ###
##################

def create_user(username,password):
        u = User.objects.create_user(username, username+"x3rus.com", password)
        u.save()

# Index
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

