from django.urls import path
from administration import views

urlpatterns = [
    path('homeAdmin/', views.homeAdmin, name='homeAdmin'), # accueil administrateur

    # _____________________________________users____________________________________________
    path('users/', views.users, name='users'),# gestion utilisateur
    path('addUser/', views.addUser, name='addUser'), # ajouter utilisateur
    path('editUser/', views.editUser, name='editUser'), # modifier utilisateur
    path('archiveUser/<int:id>/', views.archiveUser, name='archiveUser'), # modifier utilisateur
    path('editForfaitA', views.editForfaitA, name='editForfaitA'), # editer forfait

    # _____________________________________artciles____________________________________________
    path('articles/', views.articles, name='articles'), # gestion article
    path('addArticle/', views.addArticle, name='addArticle'), # ajouter article

]
