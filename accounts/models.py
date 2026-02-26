from django.db import models
from django.contrib.auth.models import (BaseUserManager,
                                        AbstractBaseUser,
                                        PermissionsMixin)
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, user_name, password, **extra_fields):
        user_name = self.model.normalize_username(user_name)
        user = self.model(user_name=user_name,  **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, user_name, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            user_name=user_name,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, user_name, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(
            user_name=user_name,
            password=password,
            **extra_fields,
        )


class User(AbstractBaseUser, PermissionsMixin):

    user_name = models.CharField(
        verbose_name=_("user_name"),
        unique=True,
        max_length=20
    )

    is_active = models.BooleanField(default=True) 
    is_staff = models.BooleanField(default=False)  

    objects = UserManager()

    USERNAME_FIELD = 'user_name'
   
    def __str__(self):
        return self.user_name 

