from database.models import Article, Category, Forfait, User
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from datetime import date, datetime
from django.contrib import messages



# Les vues de l'administrateur


def homeAdmin(request):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        
        # recuèration de l'utilisateur ici administrateur
        admin = User.objects.get(email=request.session['email'])
        
        # signalement
        signalements = Article.objects.filter(signal=True)

        # utilisateurs
        users = User.objects.filter(role=False)


        articles = Article.objects.all()

        # catégoris
        categories = Category.objects.all()

        # dictionnaire
        context = {
            'admin': admin,
            'signalements': signalements,
            'users': users,
            'articles': articles,
            'categories': categories
        }

        return render(request,'administration/homeAdmin.html', context)
    return redirect('welcome')


# gestion utilisateur
def users(request):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        admin = User.objects.get(email=request.session['email'])

        # signalement
        signalements = Article.objects.filter(signal=True)

        # _________________gestion forfaits____________________
        forfaits = []
        forfaits_data = Forfait.objects.all()

        # recupèration date actuelle
        y0, m0, d0 = str(datetime.now()).split(' ')[0].split('-')
        now = date(int(y0), int(m0), int(d0))
        

        for forfait in forfaits_data:
            y,m,d =str(forfait.end).split('-')
            if now < date(int(y), int(m), int(d)):
                forfaits.append(forfait)
        
        # résultat recherche   
        resultSearsh = ''


        # liste utilisateurs
        users_r = User.objects.filter(role=False, trash=False).order_by('id').reverse()

        paginator = Paginator(users_r, 3)

        page = request.GET.get('page')

        users = paginator.get_page(page)

        # rechercher utilisateur via email
        if request.method == 'POST':
            if 'lookUser' in request.POST:
                lookUser = request.POST['lookUser']
                users = User.objects.filter(email__startswith=lookUser, trash=False)
                resultSearsh = 'resultat recherche: '+lookUser

        articles = Article.objects.all()

        context = {
            'admin':admin,
            'page': 'users',
            'users': users,
            'resultSearsh': resultSearsh,
            'signalements': signalements,
            'forfaits': forfaits,
            'articles': articles
        }

        return render(request, 'administration/users/users.html', context)
    return redirect('welcome')


# ajouter utilisateur
def addUser(request):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        if request.method == 'POST':
            if 'firstname' and 'lastname' and 'address' and 'tel' and 'email' in request.POST and 'image' in request.FILES:
                
                # recupération données ...
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                address = request.POST['address']
                tel = request.POST['tel']
                email = request.POST['email']

                # recupèration
                users = User.objects.filter(email=email)

                # rechercher
                if len(users) != 0:
                    messages.add_message(request, messages.INFO, 'adresse email déjà existant.')
                    return redirect('users')

                if (int(tel)) <= 0 or len(str(tel)) != 9:
                    messages.add_message(request, messages.INFO, 'Numéro téléphone invalide. 9 caréctères')
                    return redirect('users')

                image = request.FILES['image']

                # creation utilisateur
                user = User()
                user.firstname = firstname.capitalize()
                user.lastname = lastname.capitalize()
                user.address = address
                user.tel = tel
                user.email = email
                user.image = image

                
                # enregistrer utilisateur
                user.save()
                messages.add_message(request, messages.INFO, 'Utilisateur créer avec succès.')
                return redirect('users')

    return redirect('welcome')


# modifier utilisateur
def editUser(request):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        if request.method == 'POST':
            
            if 'firstname' and 'id' and 'lastname' and 'address' and 'tel' and 'email' in request.POST:
                
                # recupération données ...
                id = request.POST['id']
                firstname = request.POST['firstname']
                lastname = request.POST['lastname']
                address = request.POST['address']
                tel = request.POST['tel']
                email = request.POST['email']
                image = None
                # onverifier si une image est choisie
                if 'image' in request.FILES:
                    image = request.FILES['image']

                if (int(tel)) <= 0 or len(str(tel)) != 9:
                    messages.add_message(request, messages.INFO, 'Numéro téléphone invalide. 9 caréctères')
                    return redirect('users')

                # creation utilisateur
                user = User.objects.get(id=int(id))
                user.firstname = firstname.capitalize()
                user.lastname = lastname.capitalize()
                user.address = address
                user.tel = tel
                user.email = email

                if image:
                    user.image = image

                # enregistrer utilisateur
                user.save()
                messages.add_message(request, messages.INFO, 'Utilisateur modifier avec succès.')

                return redirect('users')

    return redirect('welcome')

# archiver utilisateur
def archiveUser(request, id):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        try:
            user = User.objects.get(id = id)
            user.trash = True
            user.save()
            messages.add_message(request, messages.INFO, 'Utilisateur archiver avec succès.')
            return redirect('users')
        except User.DoesNotExist:
            return redirect('welcome')
    return redirect('welcome')

# modifer durée forfait
def editForfaitA(request):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        if request.method == "POST":
            if 'idForfait' and 'end' in request.POST:
                idForfait = int(request.POST['idForfait'])
                forfait = Forfait.objects.get(id=idForfait)
                end = request.POST['end']
                if end != 0 and str(forfait.begin) < end:
                    forfait.end = end
                    messages.add_message(request, messages.INFO, 'Forfait modifier avec succès.')
                    forfait.save()
                    return redirect('users')
                messages.add_message(request, messages.INFO, 'Date de fin forfait ne peut être inférieur à la date de début forfait.')
                return redirect('users')
            return redirect('users')
        return redirect('users')
    return redirect('welcome')
                


# articles
def articles(request):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        admin = User.objects.get(email=request.session['email'])
        # liste articles
        articles_r = Article.objects.all().order_by('id').reverse()


        paginator = Paginator(articles_r, 3)

        page = request.GET.get('page')

        articles = paginator.get_page(page)

        # catégoris
        categories = Category.objects.all()
        # dicstionnaire
        context = {
            'page': 'articles',
            'articles': articles,
            'admin': admin,
            'categories': categories
        }

        return render(request,'administration/articles/articles.html', context)


# ajouter article
def addArticle(request):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        if request.method == 'POST':
            if 'name' and 'price' and 'old_price' and 'number_of_exemplaire' and 'description' and 'category' in request.POST and  'image' in request.FILES:
                

                # admin
                admin = User.objects.get(email=request.session['email'])
                # recupèration données
                name = request.POST['name'] # nom article
                price = request.POST['price'] # prix article

                if int(price) < 0:
                    messages.add_message(request, messages.INFO, 'Prix article invalide.')
                    return redirect('articles')

                old_price = request.POST['old_price'] # ancien prix article
                if old_price and int(old_price) < 0:
                    messages.add_message(request, messages.INFO, 'Ancien prix article invalide.')
                    return redirect('articles')
                
                number_of_exemplaire = request.POST['number_of_exemplaire']
                if int(number_of_exemplaire) <= 0:
                    messages.add_message(request, messages.INFO, 'Valeur nombre exemplaires invalide.')
                    return redirect('articles')

                description = request.POST['description']
                image = request.FILES['image']

                if not request.POST['category']:
                    messages.add_message(request, messages.INFO, 'Le champ catégori est requis.')
                    return redirect('articles')
                category = Category.objects.get(id=int(request.POST['category']))

                # création d'un article
                article = Article()

                article.name = name
                article.price = price

                if old_price:
                    article.old_price = old_price
                article.number_of_exemplaire = number_of_exemplaire

                if description:
                    article.description
                article.image = image
                article.user = admin
                article.category = category
                article.save()
                messages.add_message(request, messages.INFO, 'Article enregistrer avec succès.')
                return redirect('articles')

