# Generated by Django 4.1.1 on 2023-04-15 03:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0006_likepost'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='user_name',
            field=models.CharField(blank=True, max_length=40),
        ),
    ]
