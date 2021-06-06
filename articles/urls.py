from django.urls import path
from articles import views

urlpatterns = [
    path('articles/', views.articles, name='articles'), # gestion articles
    path('saveArticle/', views.saveArticle, name='saveArticle'), # enregistrer article
    path('editArticle/<int:id>', views.editArticle, name='editArticle'), # modifier article   
]
