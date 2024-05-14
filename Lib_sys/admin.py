from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import *

# Register your models here.
class LivreDis(admin.ModelAdmin):
    list_display = ('id', 'titre', 'auteur', 'description', 'ISBN', 'langue', 'quantite')
    search_fields = ('id', 'titre', 'auteur', 'ISBN')

# Custom admin class for Client model
class ClientDis(admin.ModelAdmin):
    list_display = ('id', 'nom', 'prenom', 'date_de_naissance', 'CNI', 'date_d_inscription', 'statut')

class ExemplaireDis(admin.ModelAdmin):
    list_display = ('livre', 'numero_exemplaire', 'statut')
    search_fields = ('numero_exemplaire', 'statut')

#admin.site.register(mUser, UserAdmin)
#admin.site.register(Livre, LivreDis)
#admin.site.register(Client, ClientDis)
#admin.site.register(Exemplaire, ExemplaireDis)
#admin.site.register(Emprunt)

