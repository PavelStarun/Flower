# Generated by Django 5.0.7 on 2024-10-14 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_profile_nickname_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='telegram_nickname',
            field=models.CharField(blank=True, max_length=50, verbose_name='Никнейм в Telegram'),
        ),
    ]
