from django.contrib import admin

from .models import Pereval,Coords, Image, Level, AppUser

admin.site.register(AppUser)
admin.site.register(Pereval)
admin.site.register(Coords)
admin.site.register(Image)
admin.site.register(Level)