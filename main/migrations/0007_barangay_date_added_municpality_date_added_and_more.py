# Generated by Django 5.1.4 on 2025-01-07 06:53

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_notification_farmer_activty'),
    ]

    operations = [
        migrations.AddField(
            model_name='barangay',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='municpality',
            name='date_added',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='notification',
            name='farmer_activty',
            field=models.CharField(choices=[('', 'Select Option'), ('Rice', 'Rice'), ('Corn', 'Corn'), ('Other Crops', 'Other Crops'), ('Livestock', 'Livestock'), ('Poultry', 'Poultry'), ('Land Preparation', 'Land Preparation'), ('Planting', 'Planting'), ('Cultivation', 'Cultivation'), ('Harvesting', 'Harvesting'), ('Others', 'Others')], default='Rice', max_length=255),
        ),
    ]
