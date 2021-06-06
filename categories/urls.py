from django.urls import path
from categories import views


urlpatterns = [
    path('categories/', views.categories, name='categories'), # url pour la gestion des ctégories
    path('addCategory/', views.addCategory, name='addCategory'), # ajouter catégori
    path('editCategory/', views.editCategory, name='editCategory'), # modifier catégori
    path('deleteCategory/<int:id>', views.deleteCategory, name='deleteCategory'), # supprimer catégori
    path('saveArticleInCategory',views.saveArticleInCategory, name='saveArticleInCategory') # ajouter article
]
