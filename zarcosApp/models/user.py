from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin,BaseUserManager
from django.contrib.auth.hashers import make_password

class UserManager(BaseUserManager):
    def create_user(self, username, password = None):
        if not username:
            raise ValueError('Es necesario el nombre de usuario')
        elif not password:
            raise ValueError('Es necesario el password')
        user = self.model(username=username)
        user.set_password(password)
        user.save(using = self._db)
        return user

    def create_superuser(self, username, password = None):
        user = self.create_user(username = username, password = password)
        user.is_admin = True
        user.save(using = self._db)
        return user

class User(AbstractBaseUser,PermissionsMixin):
    id = models.BigAutoField(primary_key=True)
    username = models.CharField('Username', max_length=50, unique=True)
    password = models.CharField('Password', max_length=150)
    name = models.CharField('Name', max_length=255)
    email = models.EmailField('Email', max_length=200)

    def save(self, **kwargs):
        some_salt = 'dh74gygbhvggv'
        self.password = make_password(self.password, some_salt)
        super().save(**kwargs)

    object = UserManager()
    USERNAME_FIELD = 'username'