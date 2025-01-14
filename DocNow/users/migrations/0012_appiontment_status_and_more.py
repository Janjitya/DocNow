# Generated by Django 5.1.4 on 2025-01-02 15:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_doctor_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='appiontment',
            name='status',
            field=models.CharField(choices=[('Scheduled', 'Scheduled'), ('Completed', 'Completed'), ('Cancelled', 'Cancelled')], default='Scheduled', max_length=20),
        ),
        migrations.AlterField(
            model_name='appiontment',
            name='appointment_time',
            field=models.TimeField(),
        ),
    ]
