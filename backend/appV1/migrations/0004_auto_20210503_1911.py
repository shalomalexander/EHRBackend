# Generated by Django 3.0.8 on 2021-05-03 13:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('appV1', '0003_auto_20210503_1907'),
    ]

    operations = [
        migrations.RenameField(
            model_name='personalinfo',
            old_name='addressLine1',
            new_name='addressLine',
        ),
        migrations.RemoveField(
            model_name='personalinfo',
            name='addressLine2',
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='alternateMobileNumber',
            field=models.CharField(blank=True, max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='personalinfo',
            name='lastName',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
