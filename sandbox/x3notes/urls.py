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
                url(r'^profile/$', views.profile_user, name='profile'),
                url(r'^login/$', 'django.contrib.auth.views.login', name="login"),
                url(r'^logout/$', 'django.contrib.auth.views.logout', name="logout"),
                url(r'^(?P<username>[a-zA-Z0-9]+)/$', views.view_user, name='view_user'),
                url(r'^(?P<username>[a-zA-Z0-9]+)/addnote$', views.add_note, name='add_note'),
#                url(r'^(?P<username>[a-zA-Z0-9]+)/delnote/?P<note_id>$', views.del_note, name='del_note'),
#                url(r'^(?P<username>[a-zA-Z0-9]+)/editnote/?P<note_id>$', views.edit_note, name='edit_note'),

                # Obsolet 
                url(r'^auth/$', views.auth_user, name='auth'),
              ]
