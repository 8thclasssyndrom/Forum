from django.contrib import admin

from main.models import Fanfic, Fandom, Comment, Rating, Favorite, Like

admin.site.register(Fanfic)
admin.site.register(Fandom)
admin.site.register(Comment)
admin.site.register(Rating)
admin.site.register(Favorite)
admin.site.register(Like)

