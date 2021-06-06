from django.shortcuts import redirect, render
from database.models import User

# vue pour le module login


# connection
def login(request):
    if request.method == 'POST':
        if 'email' and 'password' in request.POST:
            
            # recupèration email et mot de passe
            email = request.POST['email']
            password = request.POST['password']

            # rechercher correspondance
            users = User.objects.filter(email=email, password=password)

            if len(users) == 1:
                user = User.objects.get(email=email, password=password)
                request.session['email'] = email
                request.session['role'] = user.role
                print('ok')
                return redirect('homeManager')
                
            else:
                return redirect('welcome')


