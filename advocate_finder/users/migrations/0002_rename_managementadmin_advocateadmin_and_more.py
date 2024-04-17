# Generated by Django 5.0.3 on 2024-03-16 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='ManagementAdmin',
            new_name='AdvocateAdmin',
        ),
        migrations.RenameModel(
            old_name='Member',
            new_name='Clients',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_management',
            new_name='is_advocate',
        ),
        migrations.RenameField(
            model_name='user',
            old_name='is_member',
            new_name='is_client',
        ),
    ]