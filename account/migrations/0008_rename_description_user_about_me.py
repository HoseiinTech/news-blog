# Generated by Django 4.1.1 on 2022-10-17 13:28

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0007_alter_user_description'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='description',
            new_name='about_me',
        ),
    ]
