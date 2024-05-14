from django.contrib.auth.models import BaseUserManager, AbstractBaseUser, PermissionsMixin
from django.db import models
import uuid

class BibliothecaireManager(BaseUserManager):
    def create_user(self, username, Nom, Prenom, password=None):
        if not username:
            raise ValueError('The Username field must be set')
        user = self.model(username=username, Nom=Nom, Prenom=Prenom)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username,Nom, Prenom, password=None):
        user = self.create_user(username=username, password=password, Nom=Nom, Prenom=Prenom)

        return user
