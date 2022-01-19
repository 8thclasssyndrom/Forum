from django.contrib import admin

from main.models import Fanfic, Fandom, Comment, Rating

admin.site.register(Fanfic)
admin.site.register(Fandom)
admin.site.register(Comment)
admin.site.register(Rating)

