from django.db import models
from django_resized import ResizedImageField

# _______________ mes modéles _______________



# Modéle User => qui va avoir un role admin (True) ou utilsateur simple (False)
class User(models.Model):
    firstname = models.CharField(max_length=255) # prenom 
    lastname = models.CharField(max_length=255) # nom
    address = models.CharField(max_length=255) # adresse
    tel = models.CharField(max_length=255) # téléphone
    email = models.CharField(max_length=255, unique=True) # mail
    password = models.CharField(max_length=255) # mot de passe
    role = models.BooleanField(default=False) # role: True => admin ou False => simple utilisateur
    image = ResizedImageField(size=[60, 50], upload_to='profils')

    def __str__(self):
        return self.firstname+ ' ' +self.lastname


# Modéle Catégory
class Category(models.Model):
    name = models.CharField(max_length=255, unique=True) # nom catégori
    description = models.TextField() # description
    created_at = models.DateField(auto_now=True) # date de création
    updated_at = models.DateField(auto_now_add=True) # datede mise à jour
    user = models.ForeignKey(User, on_delete=models.CASCADE) # utilisateur créateur

    def __str__(self):
        return self.name

# Modéle Article
class Article(models.Model):
    name = models.CharField(max_length=255) # nom de l'article
    price = models.PositiveBigIntegerField() # prix de l'article
    old_price = models.PositiveBigIntegerField(null=True, blank=True) # prix de l'article evant
    number_of_exemplaire = models.PositiveIntegerField() # nombre d'exemplaire
    description = models.TextField(null=True,blank=True) # description
    user = models.ForeignKey(User, on_delete=models.CASCADE) # utilisateur créateur
    category = models.ForeignKey(Category, on_delete=models.CASCADE) # catégori de l'article
    image = ResizedImageField(size=[500, 300], upload_to='images')

    def __str__(self):
        return self.name