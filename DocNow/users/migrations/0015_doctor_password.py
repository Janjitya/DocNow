# Generated by Django 5.1.4 on 2025-01-05 14:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_alter_profile_photo'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctor',
            name='password',
            field=models.CharField(default=0, max_length=128),
            preserve_default=False,
        ),
    ]
