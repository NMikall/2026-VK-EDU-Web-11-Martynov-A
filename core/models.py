from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name="Пользователь")
    avatar = models.ImageField(upload_to='avatars/%Y/%m', verbose_name="Аватар пользователя", default="avatar.webp")
    nickname = models.CharField(max_length=20, verbose_name="Ник пользователя")

    def __str__(self):
        return self.nickname

    class Meta:
        verbose_name = "Профиль"
        verbose_name_plural = "Профили"