# Generated by Django 3.1.2 on 2020-10-15 21:24

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0002_post'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='likes',
            field=models.ManyToManyField(null=True, related_name='likes', to=settings.AUTH_USER_MODEL),
        ),
    ]
