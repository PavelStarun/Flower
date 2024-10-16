from django.db import models
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    birth_date = models.DateField(null=True, blank=True)
    telegram_nickname = models.CharField(max_length=50, blank=True, verbose_name="Никнейм в Telegram")

    def __str__(self):
        return f'{self.user.username} Profile'
