# Generated by Django 4.1.3 on 2022-11-25 01:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('search', '0003_user_bio_user_email'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='bio',
            field=models.TextField(blank=True),
        ),
        migrations.AlterField(
            model_name='user',
            name='email',
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
