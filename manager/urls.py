from django.urls import path
from manager import views

# ici nous aurons les urls pour le manager du site
urlpatterns = [
    path('homeManager/', views.homeManager, name='homeManager'),
    path('deleteArticle/<int:id>', views.deleteArticle, name='deleteArticle'),
]
