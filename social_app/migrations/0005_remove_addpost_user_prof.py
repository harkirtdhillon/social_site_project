# Generated by Django 4.1.1 on 2023-04-12 15:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('social_app', '0004_alter_addpost_user_prof'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='addpost',
            name='user_prof',
        ),
    ]
