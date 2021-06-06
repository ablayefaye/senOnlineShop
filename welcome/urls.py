from django.urls import path
from welcome import views


urlpatterns = [
    path('welcome/', views.welcome, name='welcome'), # page accueil site
    path('welcome_articles', views.welcome_articles, name='welcome_articles'), # publication des articles
]
