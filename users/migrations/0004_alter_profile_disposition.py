# Generated by Django 4.0.2 on 2022-02-20 15:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0003_alter_profile_life_pattern_alter_profile_mbti_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='disposition',
            field=models.CharField(blank=True, choices=[('collective', '집단주의'), ('individual', '개인주의')], max_length=10),
        ),
    ]
