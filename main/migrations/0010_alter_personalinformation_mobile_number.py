# Generated by Django 5.1.4 on 2025-01-20 15:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_personalinformation_middlename'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalinformation',
            name='mobile_number',
            field=models.CharField(help_text='Mobile Number', max_length=11, unique=True),
        ),
    ]
