# Generated by Django 3.2.11 on 2024-03-20 17:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('favorites', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='favorite',
            old_name='article',
            new_name='blog',
        ),
    ]
