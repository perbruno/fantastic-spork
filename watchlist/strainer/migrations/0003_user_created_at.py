# Generated by Django 3.1.6 on 2021-02-10 13:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('strainer', '0002_auto_20210210_1308'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='created_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
