# Generated by Django 3.2.11 on 2024-03-19 21:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_alter_profile_profile_photo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='facebook_account',
            field=models.CharField(blank=True, max_length=50, verbose_name='facebook_account'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='github_account',
            field=models.CharField(blank=True, max_length=50, verbose_name='twitter_account'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='twitter_handle',
            field=models.CharField(blank=True, max_length=50, verbose_name='twitter_handle'),
        ),
    ]
