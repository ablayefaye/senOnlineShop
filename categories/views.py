from articles.forms import SaveArticleForm, SaveArticleFormInCategory
from database.models import Article, Category, User
from django.shortcuts import redirect, render
from django.contrib import messages #import messages

# vues pour catgegy


def categories(request):
    if 'email' and 'role' in request.session and request.session['role'] == True:

        # utilisateur connecté
        user = User.objects.get(email=request.session['email'])


        # liste catégories
        categories = Category.objects.all().order_by('id').reverse()

        # liste articles
        articles = Article.objects.all()

        form = SaveArticleFormInCategory(request.POST or None)
        # dictionnaire
        context = {
            'user': user,
            'page': 'categories',
            'categories': categories,
            'articles': articles,
            'form': form
        }

        return render(request,'categories/categorie.html', context)
    return redirect('welcome')


def addCategory(request):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        if request.method == 'POST':
            if 'user' and 'name' and 'description' in request.POST:

                # recuperer utilisteur
                user = User.objects.get(id=int(request.POST['user']))
                # nom catégori
                name = request.POST['name']
                # description catégori
                description = request.POST['description']

                #  creation catégori
                category = Category()
                category.name = name
                category.description = description
                category.user = user

                # enregitrement catégori
                category.save()         

                # redirection avec message ...  
                messages.success(request, 'Catégori ajouté avec succés.')
                return redirect('categories')
    return redirect('welcome')


def editCategory(request):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        if request.method == 'POST':
            if 'name' and 'description' and 'id' in request.POST:
                
                # recupèrer nom
                name = request.POST['name']

                # recupèrer description
                description = request.POST['description']

                # recupèrer id 
                id = request.POST['id']

                # recupèrer catégori correspondant
                category = Category.objects.get(id=int(id))
                
                category.name = name
                category.description = description

                # enregistrer modifications
                category.save()

                messages.success(request, 'Catégori #'+ str(category.id) +' modifié avec succé.')
                return redirect('categories')

    return redirect('welcome')


def deleteCategory(request, id):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        try:
            # suppression catégori
            category = Category.objects.get(id=id)
            category.delete()
            messages.success(request, 'Catégori '+ category.name +' supprimé avec succés.')
            return redirect('categories')
        except Category.DoesNotExist:
            return redirect('categories')
    return redirect('welcome')


# enregistrer article
def saveArticleInCategory(request):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        if request.method == 'POST':
            # if 'name' in request.POST:
                # print(request.POST['cate'])
            form = SaveArticleFormInCategory(request.POST or None, request.FILES)
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
                    return redirect('categories')
                else:
                    messages.success(request, 'prix, ancien prix article et nombre exemplaires article doivent être positifs')
                    return redirect('categories') 
            else:
                # vérifier données
                if int(article.price) > 0 and int(article.number_of_exemplaire) > 0:
                    article.save()
                    messages.success(request, 'Article ajouté avec succé.')
                    return redirect('categories')
                else:
                    messages.success(request, 'prix, prix article et nombre exemplaires article doivent être positifs')
                    return redirect('categories')

    return redirect('welcome')
