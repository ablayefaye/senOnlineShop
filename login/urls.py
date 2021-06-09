from django.urls import path
from login.views import *

urlpatterns = [
    path('login/', login, name='login'), # connexion à l'application
    path('disconnect/', disconnect, name='disconnect')
]
