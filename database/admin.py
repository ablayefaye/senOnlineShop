from database.models import Article, Category, User
from django.contrib import admin
from database.models import *


# les modéles à registrer
admin.site.register(User)
admin.site.register(Article)
admin.site.register(Category)
