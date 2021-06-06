from django.shortcuts import redirect, render
from database.models import Article, User
from django.contrib import messages #import messages

# ici nous avons les vue de manager


# page accueil manager
def homeManager(request):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        
        # utilisateur connecté
        user = User.objects.get(id=1)

        # la liste des articles (par les plus récent)
        articles = Article.objects.all().order_by('id').reverse()

        # dictionnaire python
        context = {
            'user': user,
            'articles': articles,
            'page': 'manager'
        }
        return render(request,'manager/homeManager.html', context)
    return redirect('welcome')


# supprimer un article
def deleteArticle(request, id):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        try:
            Article.objects.get(id=id).delete()
            messages.success(request, "Article supprimer avec succé." )
            return redirect ('homeManager')
        except Article.DoesNotExist:
            return redirect('homeManager')
    return redirect('welcome')