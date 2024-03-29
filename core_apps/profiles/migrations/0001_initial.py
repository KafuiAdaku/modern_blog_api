# Generated by Django 3.2.11 on 2024-03-17 04:11

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('pkid', models.BigAutoField(editable=False, primary_key=True, serialize=False)),
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('about_me', models.TextField(default='', verbose_name='about me')),
                ('gender', models.CharField(choices=[('male', 'male'), ('female', 'female'), ('other', 'other')], default='other', max_length=20, verbose_name='gender')),
                ('city', models.CharField(default='Accra', max_length=180, verbose_name='city')),
                ('profile_photo', models.ImageField(default='/profile_default.png', upload_to='', verbose_name='profile photo')),
                ('twitter_handle', models.CharField(blank=True, max_length=20, verbose_name='twitter_handle')),
                ('facebook_handle', models.CharField(blank=True, max_length=20, verbose_name='twitter_handle')),
                ('github_handle', models.CharField(blank=True, max_length=20, verbose_name='twitter_handle')),
                ('follows', models.ManyToManyField(blank=True, related_name='followed_by', to='profiles.Profile')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created_at', '-updated_at'],
                'abstract': False,
            },
        ),
    ]
