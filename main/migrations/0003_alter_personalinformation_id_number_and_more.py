# Generated by Django 5.1.4 on 2024-12-08 12:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0002_alter_personalinformation_member_in_ip_specific'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalinformation',
            name='id_number',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='is_member_in_ip',
            field=models.BooleanField(blank=True, default=False, help_text='Member of an Indigenous Group', null=True),
        ),
        migrations.AlterField(
            model_name='personalinformation',
            name='type_of_id',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
