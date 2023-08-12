from django.contrib import admin
from .models import Member, Photo

class MemberAdmin(admin.ModelAdmin):
    list_display = ("primeiroNome", "ultimoNome", "data_acesso")

class PhotosAdmin(admin.ModelAdmin):
    list_display = ("nome", "comentario", "foto")

admin.site.register(Member, MemberAdmin)
admin.site.register(Photo, PhotosAdmin)
