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
# Create your tests here.


##################
### VIEW tests ###
##################

# Index
class IndexViewTests(TestCase):
    def test_index_view_with_no_users(self):
        """
        If no users exist, an appropriate message should be displayed.
        """
        response = self.client.get(reverse('x3notes:index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "show")
