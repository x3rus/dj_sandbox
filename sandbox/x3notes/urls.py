# Description :
#       Header pour l'application X3notes
#   
# 
# Auteur : Boutry Thomas <thomas.boutry@x3rus.com>
# Date de creation : 2015-06-30
# Licence : GPL v3.
###############################################################################


from django.conf.urls import url

from . import views

urlpatterns = [
#                url(r'^$', views.IndexView.as_view(), name='index'),
                url(r'^$', views.index, name='index'),
              ]
