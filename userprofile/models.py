from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user = models.OneToOneField(User)
    avatar = models.ImageField(upload_to='user_avatars', blank=True)
    number = models.CharField(max_length=100, blank=True)

User.profile = property(lambda u: UserProfile.objects.get_or_create(user=u)[0])
