import requests
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models


class LinkManager(models.Manager):

    def create(self, url):
        response = requests.get('http://127.0.0.1:8000/api/keys/')
        if response.status_code != 200:
            raise Exception(response.content)

        short_url = response.json()['base62']
        link = Link(short_url=short_url, url=url, view_count=0)
        link.save()
        return link


class Link(models.Model):

    url = models.TextField()
    short_url = models.TextField(blank=True)
    view_count = models.IntegerField(default=0)

    objects = LinkManager()

    class Meta:
        db_table = 'link'


class LinkMember(models.Model):

    link = models.ForeignKey(Link, on_delete=models.CASCADE)
    user = models.ForeignKey('User', on_delete=models.CASCADE)

    class Meta:
        db_table = 'link_member'


class UserManager(BaseUserManager):

    def create_user(self, title, email, password):
        user = self.model(title=title, email=email)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, title, email, password):
        user = self.create_user(
            title=title,
            email=email,
            password=password,
        )
        user.is_admin = True
        user.save()
        return user


class User(AbstractBaseUser, PermissionsMixin):

    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_system = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    password = models.CharField(max_length=255)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['title']

    def has_perm(self, perm, obj=None):
        """Does the user have a specific permission?"""
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        """Does the user have permissions to view the app `app_label`?"""
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        """Is the user a member of staff?"""
        # Simplest possible answer: All admins are staff
        return self.is_admin

    class Meta:
        db_table = 'user'
        verbose_name_plural = 'user'
        ordering = ['id']

