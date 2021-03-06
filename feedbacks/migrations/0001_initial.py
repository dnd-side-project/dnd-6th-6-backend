# Generated by Django 4.0.2 on 2022-02-15 01:10

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('chores', '0005_choreinfo_house'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=255)),
                ('content', models.CharField(max_length=255)),
                ('sended_at', models.DateTimeField(auto_now_add=True)),
                ('_from', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', related_query_name='has_feedback', to=settings.AUTH_USER_MODEL)),
                ('chore', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedbacks', related_query_name='feedback', to='chores.chore')),
            ],
        ),
    ]
