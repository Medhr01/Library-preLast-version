from typing import Iterable
from django.db import models
from datetime import *
from .managers import BibliothecaireManager
import uuid
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, AbstractUser
from django.db.models.signals import post_save, pre_save, post_delete
from django.dispatch import receiver

class bibliothecaire(AbstractBaseUser):
    Identifient = models.CharField(max_length=20, unique=True, editable=False)
    Nom = models.CharField(max_length=50, blank=True, null=True)
    Prenom = models.CharField(max_length=50, blank=True, null=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    objects = BibliothecaireManager()
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ['Nom', 'Prenom', "is_staff"]

    def save(self, *args, **kwargs):
        if not self.Identifient:
            r = str(uuid.uuid4().int)[:6]
            self.Identifient = 'ADM' + r
        super().save(*args, **kwargs)

class Bouquin(models.Model):
    LANGUE_CHOICES = [
        ('', 'Select langue'),
        ('AR','Arabe'),
        ('FR', 'Français'),
        ('EN', 'Anglais'),
        ('ES', 'Espagnol'),
        ('AUTRE', 'Autre'),
    ]
    STATUT_CHOICES = [
        ('Disponible pour prêt', 'Disponible'),
        ('Hors prêt', 'Hors prêt')
    ]
    Titre = models.CharField(max_length=100)
    Auteur = models.CharField(max_length=100)
    Description = models.TextField(blank=True)
    ISBN = models.CharField(max_length=13, unique=True, help_text="must be unique",)
    Langue = models.CharField(max_length=6, choices=LANGUE_CHOICES)
    Quantite_achete = models.PositiveBigIntegerField(default=0)
    Quantite_Disponible  = models.PositiveIntegerField(default=0)
    Statut = models.CharField(max_length=50, default="Disponible pour prêt", choices=STATUT_CHOICES)
    Cover = models.ImageField(upload_to="Bouquin/", default="/cover.jpg")
    
    def __str__(self):
        return f"{self.Titre}"
    
    def prett(self, act):
        if act == "oui":
            self.Statut = "Disponible pour prêt"
        else:
            self.Statut = "Hors prêt"
        self.save()

class Client(models.Model):
    STATUT_CHOICES = [
        ('Active', 'Active'),
        ('Non active', 'Non active'),
        ('Banned', 'Banned'),
    ]

    Nom = models.CharField(max_length=100)
    Prenom = models.CharField(max_length=100)
    Date_de_naissance = models.DateField()
    CNI = models.CharField(max_length=20, unique=True)
    Date_d_inscription = models.DateField(auto_now_add=True)
    Statut = models.CharField(max_length=50, default="Active")
    image = models.ImageField(upload_to="clients/", default="/client.png")

    def __str__(self):
        return f'{self.Nom} {self.Prenom}'
    
    def activer(self):
        self.Statut ="Active"
        self.save()
        
    def desactiver(self):
        self.Statut ="Non active"
        self.save()

class Exemplaire(models.Model):
    STATUT_CHOICES = [('Disponible', 'Disponible'),
                    ('Perdu', 'Perdu'),
                    ('Endommagé', 'Endommagé'),
                    ('Prêté', 'Prêté')]
    Bouquin = models.ForeignKey('Bouquin', on_delete=models.CASCADE)
    Id_exemplaire = models.CharField(max_length=100)
    Statut = models.CharField(max_length=50, default='Disponible')

    def __str__(self):
        return f"<b>{self.Bouquin.Titre}</b> / {self.Id_exemplaire}"
    
    def emprunt_exmp(self):
        self.Statut = 'Prêté'
        self.save()

    def renouvler(self):
        self.Statut = 'Disponible'
        self.save()

    def retirer(self):
        self.delete()

    def perdu(self):
        self.Statut = "Perdu"
        self.save()

@receiver(post_save, sender=Exemplaire)
@receiver(post_delete, sender=Exemplaire)
def auto_update_number_exemplaires(sender, instance, **kwargs):
    livre = instance.Bouquin
    dispo_exmp = Exemplaire.objects.filter(Bouquin=livre, Statut='Disponible').count()
    livre.Quantite_Disponible = dispo_exmp
    livre.save()

@receiver(post_save, sender=Bouquin)
def auto_create_exemplaires(sender, instance, created, **kwargs):
    if created:
        for i in range(instance.Quantite_achete):
            Exemplaire.objects.create(
                Bouquin=instance,
                Id_exemplaire=f"{instance.ISBN}-{i + 1}",
                Statut='Disponible'
            )

class Emprunt(models.Model):
    Exemplaire = models.ForeignKey('Exemplaire', on_delete=models.CASCADE)
    Client = models.ForeignKey('Client', on_delete=models.CASCADE)
    bibliothecaire = models.ForeignKey('bibliothecaire', on_delete=models.CASCADE)
    Date_emprunt = models.DateField(auto_now_add=True)
    Date_retour =  models.DateField()
    Retourne = models.CharField(default="-", max_length=50)

    def return_exmp(self, etat):
        if etat == "v":
            self.Exemplaire.Statut = 'Disponible'
        else:
            self.Exemplaire.Statut = 'Endommagé'
        self.Exemplaire.save()
        self.Retourne = str(datetime.today().strftime("%d/%m/%Y"))
        self.save()
    
    def perdu(self):
        self.Retourne = self.Exemplaire.Statut = "Perdu"
        self.save()
        self.Exemplaire.save()