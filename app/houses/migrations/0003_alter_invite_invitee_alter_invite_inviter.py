# Generated by Django 4.0.2 on 2022-02-09 14:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('houses', '0002_invite'),
    ]

    operations = [
        migrations.AlterField(
            model_name='invite',
            name='invitee',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='received_invites', related_query_name='received_invite', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='invite',
            name='inviter',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sent_invites', related_query_name='sent_invite', to=settings.AUTH_USER_MODEL),
        ),
    ]
