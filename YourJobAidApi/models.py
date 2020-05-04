from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager, Group

from django.utils.timesince import timesince

from django.conf import settings
from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from .slugify import unique_slug_generator


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


class UserProfileManager(BaseUserManager):
    """Manager for user profiles"""

    def create_user(self, email, name, password=None):
        """Create a new user profile"""
        if not email:
            raise ValueError('Users must have an email address')

        email = self.normalize_email(email)
        user = self.model(email=email, name=name )

        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, name, password):
        """Create and save a new superuser with given details"""
        user = self.create_user(email, name, password)
        user.is_superuser = True
        user.is_staff = True
        user.save(using=self._db)

        return user

def user_profile_picture_directory_path(instance, filename):
        return 'user_{0}/{1}'.format(instance.id, filename)

class UserProfile(AbstractBaseUser, PermissionsMixin):
    """Database model for users in the system"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    bio = models.TextField(max_length=1000, null=True, blank=True,default="No data to show.")

    group = models.ForeignKey(Group, on_delete=models.CASCADE, related_name='role', null=True,blank=True)
    profile_pic = models.ImageField(upload_to=user_profile_picture_directory_path,
                                    height_field=None,
                                    width_field=None,
                                    max_length=100, default="default_pro_pic/dp.png")
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserProfileManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']

    def get_full_name(self):
        """Retrieve full name for user"""
        return self.name

    def get_short_name(self):
        """Retrieve short name of user"""
        return self.name



    def __str__(self):
        """Return string representation of user"""
        return self.name




class Category(models.Model):
    title = models.CharField(max_length=255, null=True, blank=True)
    slug = models.SlugField(max_length=300, blank=True, unique=True)

    def __str__(self):
        return self.title


@receiver(pre_save, sender=Category)
def create_auto_slug_category(sender, instance=None, created=False, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)


class Post(models.Model):

    title = models.CharField(max_length=1000, null=True, blank=True)
    slug = models.SlugField(max_length=300, null=True, blank=True, unique=True)
    img = models.ImageField(upload_to="jobs/%Y/%m/%d/", height_field=None,
                                    width_field=None,
                                    max_length=100, default="jobaid_default_post_pic/yourjobaid.jpg")
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, default=1)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='totalposts')
    meta = models.CharField(max_length=100, null=True, blank=True)
    description = models.TextField(max_length=5000, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_date(self):
        time = str(timesince(self.created_at)) + " ago"
        return time

    def __str__(self):
        return self.title + ' - ' + str(self.user)


class Comment(models.Model):
    user = models.ForeignKey(UserProfile, on_delete=models.CASCADE, null=True, blank=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True)
    text = models.TextField(max_length=1000)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_time(self):
        time = str(timesince(self.created_at)) + " ago"
        return time

    def children(self):
        return Comment.objects.filter(parent=self)

    @property
    def is_parent(self):
        if self.parent is not None:
            return False
        return True

    def __str__(self):
        return self.text





@receiver(pre_save, sender=Post)
def create_auto_slug_post(sender, instance=None, created=False, **kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)







class ContactUs(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(max_length=255, null=True, blank=True)
    message = models.TextField(max_length=5000, null=True, blank=True)
    is_seen = models.BooleanField(default=False, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    email_isSent = models.BooleanField(default=True,blank=True)

    def __str__(self):
        return self.name + ' - ' + self.email
