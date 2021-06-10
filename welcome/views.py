from database.models import Article, Category, User
from django.shortcuts import redirect, render

# Create your views here.

# accueil site
def welcome(request):
    # request.session['email'] = 'layefayenevrose@gmail.com'
    # request.session['role'] = True
    user = None
    if 'email' and 'role' in request.session and request.session['role'] == True:
        user = User.objects.get(email=request.session['email']) 
    
    # liste articles
    articles = Article.objects.all().order_by('id').reverse()

    context = {
         'user': user,
         'articles': articles,
         'page': 'welcome'
    }
    return render(request,'welcome/welcome.html', context)

def welcome_articles(request):
    
    # initialisation ...
    user = None

    if 'email' and 'role' in request.session and request.session['role'] == True:
        user = User.objects.get(email=request.session['email'])

    # liste catégoris
    categories = Category.objects.all()

    # liste articles
    articles = Article.objects.all().order_by('id').reverse()

    # initialisation ...
    category = None

    # recupération catégories
    if 'category' in request.GET:
        category_name = request.GET['category']

        if category_name == 'all':
            articles = Article.objects.all().order_by('id').reverse()
        else:
            category = Category.objects.get(name=category_name) 
            articles = category.article_set.all()
    context = {
        'page': 'welcome_articles',
        'categories': categories,
        'articles': articles,
        'category': category,
        'user': user,
    }
    return render(request, 'welcome/welcome_articles.html', context)