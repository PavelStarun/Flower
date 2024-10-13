# Generated by Django 5.1.2 on 2024-10-12 09:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_profile_nickname_profile_telegram_nickname'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='nickname',
        ),
        migrations.AddField(
            model_name='profile',
            name='login',
            field=models.CharField(blank=True, max_length=50, verbose_name='Логин'),
        ),
    ]