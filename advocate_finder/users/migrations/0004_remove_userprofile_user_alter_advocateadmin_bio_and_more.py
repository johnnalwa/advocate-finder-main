# Generated by Django 5.0.3 on 2024-03-19 19:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_practicearea_rename_create_at_clients_created_at_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userprofile',
            name='user',
        ),
        migrations.AlterField(
            model_name='advocateadmin',
            name='bio',
            field=models.TextField(blank=True, max_length=1000, null=True),
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(blank=True, max_length=255, null=True)),
                ('last_name', models.CharField(blank=True, max_length=255, null=True)),
                ('physical_address', models.TextField(blank=True, max_length=255, null=True)),
                ('national_id', models.CharField(blank=True, max_length=255, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=255, null=True)),
                ('year_of_birth', models.CharField(blank=True, max_length=4, null=True)),
                ('gender', models.CharField(blank=True, max_length=10, null=True)),
                ('profile_img', models.ImageField(blank=True, default='default.png', null=True, upload_to='Profile')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Case',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('description', models.TextField()),
                ('status', models.CharField(default='Pending', max_length=20)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('lawyer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.lawyerprofile')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='users.client')),
            ],
        ),
        migrations.DeleteModel(
            name='Clients',
        ),
        migrations.DeleteModel(
            name='UserProfile',
        ),
    ]
