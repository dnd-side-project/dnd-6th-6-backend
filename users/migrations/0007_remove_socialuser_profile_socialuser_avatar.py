# Generated by Django 4.0.2 on 2022-02-21 20:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_alter_profile_user'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='socialuser',
            name='profile',
        ),
        migrations.AddField(
            model_name='socialuser',
            name='avatar',
            field=models.URLField(default=''),
        ),
    ]
