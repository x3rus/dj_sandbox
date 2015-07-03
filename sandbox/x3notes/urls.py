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
                url(r'^$', views.IndexView.as_view(), name='index'),
#                url(r'^(?P<username>[a-zA-Z0-9]+)/$', views.viewuser(), name='viewuser'),
                url(r'^auth/$', views.auth_user, name='auth'),
                url(r'^profile/$', views.profile_user, name='profile'),
                url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
                url(r'^logout/$', 'django.contrib.auth.views.logout', name="logout"),
              ]
