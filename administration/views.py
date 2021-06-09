from database.models import Article, Category, Forfait, User
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from datetime import date, datetime
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
                users = User.objects.filter(email=lookUser, trash=False)
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
                return redirect('users')

    return redirect('welcome')

# archiver utilisateur
def archiveUser(request, id):
    if 'email' and 'role' in request.session and request.session['role'] == True:
        try:
            user = User.objects.get(id = id)
            user.trash = True
            user.save()
            return redirect('users')
        except User.DoesNotExist:
            return redirect('welcome')
    return redirect('login')

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
                    forfait.save()
                return redirect('users')