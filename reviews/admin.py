from django.contrib import admin
from .models import Review, Game, Tag

admin.site.register(Review)
admin.site.register(Tag)
admin.site.register(Game)
