from categories.views import addCategory
from django.shortcuts import redirect, render
from database.models import *
from .forms import *
from django.contrib import messages #import messages



# gestion articles
def articles(request):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        
        # catégori filtrer
        category = ''

        # utilisateur connecté
        user = User.objects.get(email=request.session['email'])

        # liste articles
        articles = Article.objects.all().order_by('id').reverse()

        # liste categories
        categories = Category.objects.all().order_by('id').reverse()

        # formualire création articles
        form = SaveArticleForm(request.POST or None)
        # dictionnaire ...

        # filtrer catégories
        if 'category' in request.GET:
            category_name = request.GET['category']
            if category_name == 'all':
                articles = Article.objects.all().order_by('id').reverse()
            else:
                category = Category.objects.get(name=category_name)                
                articles = category.article_set.all()


        context = {
            'articles': articles,
            'form': form,
            'user': user,
            'categories': categories,
            'category': category,
            'page': 'articles'
        }
        # formulaire pour enregistré article
        
        
        return render(request,'articles/articles.html', context)
    return redirect('welcome')


# enregistrer article
def saveArticle(request):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        if request.method == 'POST':
            # if 'name' in request.POST:
                # print(request.POST['cate'])
            form = SaveArticleForm(request.POST or None, request.FILES)
            # création d'un article
            article = Article()
            article.name =  request.POST['name']
            if request.POST['old_price']:
                article.old_price = request.POST['old_price']
            article.price = request.POST['price']
            article.user = User.objects.get(email=request.session['email'])
            article.number_of_exemplaire = request.POST['number_of_exemplaire']
            if request.POST['description']:
                article.description = request.POST['description'] 

            article.category = Category.objects.get(id=int(request.POST['category']))
            article.image = request.FILES['image']

            if article.old_price:
                # vérifier données
                if int(article.price) > 0 and int(article.old_price) > 0 and int(article.number_of_exemplaire) > 0:
                    article.save()
                    messages.success(request, 'Article ajouté avec succés.')
                    return redirect('articles')
                else:
                    messages.success(request, 'prix, ancien prix article et nombre exemplaires article doivent être positifs')
                    return redirect('articles') 
            else:
                # vérifier données
                if int(article.price) > 0 and int(article.number_of_exemplaire) > 0:
                    article.save()
                    messages.success(request, 'Article ajouté avec succé.')
                    return redirect('articles')
                else:
                    messages.success(request, 'prix, prix article et nombre exemplaires article doivent être positifs')
                    return redirect('articles')

    return redirect('welcome')

# modifier article
def editArticle(request, id):
    if 'email' and 'role' in request.session and request.session['role'] == True:

        # recupèrer article
        article = Article.objects.get(id=id)

        form = SaveArticleForm(request.POST or None, instance=article)

        if request.method == 'POST':
            form = SaveArticleForm(request.POST or None ,request.FILES,instance=article)
            price = request.POST['price']
            old_price = request.POST['old_price']
            number_of_exemplaire = request.POST['number_of_exemplaire']
            try:
                int(old_price)
                int(price)
                int(number_of_exemplaire)
                pass
            except:
                messages.success(request, 'valeur invalide.')
                return redirect('editArticle', id)
            number_of_exemplaire = request.POST['number_of_exemplaire']
            article.name =  request.POST['name']
            article.number_of_exemplaire = request.POST['number_of_exemplaire']
            article.category = Category.objects.get(id=int(request.POST['category']))
            article.image = request.FILES['image']
            article.description = request.POST['description']
            if old_price:
                # vérifier données
                if int(price) > 0 and int(old_price) > 0 and int(number_of_exemplaire) > 0:
                        article.save()
                        messages.success(request, 'Article modifier avec succés.')
                        return redirect('articles')
                else:
                    messages.success(request, 'prix, ancien prix article et nombre exemplaires article doivent être positifs')
                    return redirect('editArticle', id) 
            else:
                # vérifier données
                if int(price) > 0 and int(number_of_exemplaire) > 0:
                    article.save()
                    messages.success(request, 'Article modifier avec succé.')
                    return redirect('articles')

        
        context = {
            'form': form,
            'article': article,
            'page': 'articles'
        }
        return render(request, 'articles/editArticle.html', context)
    return redirect('welcome')    
