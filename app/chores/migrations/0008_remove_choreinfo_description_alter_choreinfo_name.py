# Generated by Django 4.0.2 on 2022-02-19 00:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chores', '0007_alter_chore_options'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='choreinfo',
            name='description',
        ),
        migrations.AlterField(
            model_name='choreinfo',
            name='name',
            field=models.CharField(max_length=255),
        ),
    ]