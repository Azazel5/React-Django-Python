# Generated by Django 3.0.5 on 2020-05-08 21:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('imageapi', '0003_auto_20200508_1320'),
    ]

    operations = [
        migrations.AddField(
            model_name='userimages',
            name='image',
            field=models.ImageField(null=True, upload_to='UserImages'),
        ),
    ]
