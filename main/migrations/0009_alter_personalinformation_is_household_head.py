# Generated by Django 5.1.4 on 2024-12-08 17:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0008_alter_personalinformation_is_member_in_ip'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalinformation',
            name='is_household_head',
            field=models.BooleanField(default=True),
        ),
    ]
