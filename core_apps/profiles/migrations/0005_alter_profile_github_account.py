# Generated by Django 3.2.11 on 2024-03-20 15:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0004_auto_20240319_2136'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='github_account',
            field=models.CharField(blank=True, max_length=50, verbose_name='github_account'),
        ),
    ]
