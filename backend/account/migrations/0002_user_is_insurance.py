# Generated by Django 3.2.2 on 2021-06-25 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='is_insurance',
            field=models.BooleanField(default=False),
        ),
    ]
