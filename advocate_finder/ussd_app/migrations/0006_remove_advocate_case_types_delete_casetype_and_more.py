# Generated by Django 5.0.3 on 2024-04-16 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ussd_app', '0005_casetype_remove_advocate_case_types_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='advocate',
            name='case_types',
        ),
        migrations.DeleteModel(
            name='CaseType',
        ),
        migrations.AddField(
            model_name='advocate',
            name='case_types',
            field=models.CharField(default=1, max_length=200),
            preserve_default=False,
        ),
    ]
