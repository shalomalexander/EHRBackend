# Generated by Django 3.0.8 on 2021-04-27 07:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appV1', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='medicalpractitionerinfo',
            name='activeIndicator',
            field=models.CharField(choices=[('Y', 'YES'), ('N', 'NO')], default='N', max_length=1),
        ),
    ]
