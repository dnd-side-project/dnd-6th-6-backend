# Generated by Django 4.0.2 on 2022-02-21 16:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('notifications', '0007_alter_notificationfavor_created_at_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='notificationfavor',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='notificationfeedback',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='notificationinvite',
            options={'ordering': ['-created_at']},
        ),
        migrations.AlterModelOptions(
            name='notificationnotice',
            options={'ordering': ['-created_at']},
        ),
    ]
