from django.urls import path
from administration import views

urlpatterns = [
    path('homeAdmin/', views.homeAdmin, name='homeAdmin'), # accueil administrateur
    path('users/', views.users, name='users'),# gestion utilisateur
    path('addUser/', views.addUser, name='addUser'), # ajouter utilisateur
    path('editUser/', views.editUser, name='editUser'), # modifier utilisateur
    path('archiveUser/<int:id>/', views.archiveUser, name='archiveUser'), # modifier utilisateur
    path('editForfaitA', views.editForfaitA, name='editForfaitA') # editer forfait
]
