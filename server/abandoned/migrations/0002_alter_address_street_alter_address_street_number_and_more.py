# Generated by Django 4.2.2 on 2023-06-09 10:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('abandoned', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='address',
            name='street',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='street_number',
            field=models.CharField(blank=True, max_length=4, null=True),
        ),
        migrations.AlterField(
            model_name='address',
            name='zipcode',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
    ]
