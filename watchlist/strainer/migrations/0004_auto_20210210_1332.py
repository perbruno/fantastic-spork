# Generated by Django 3.1.6 on 2021-02-10 13:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('strainer', '0003_user_created_at'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='created_at',
            new_name='updated_at',
        ),
    ]