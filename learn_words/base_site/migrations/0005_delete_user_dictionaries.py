# Generated by Django 4.1.7 on 2023-08-23 23:46

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base_site', '0004_alter_user_dictionaries_username'),
    ]

    operations = [
        migrations.DeleteModel(
            name='User_Dictionaries',
        ),
    ]