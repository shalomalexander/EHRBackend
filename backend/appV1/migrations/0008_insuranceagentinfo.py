# Generated by Django 3.2.2 on 2021-06-25 11:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0002_user_is_insurance'),
        ('appV1', '0007_auto_20210625_1147'),
    ]

    operations = [
        migrations.CreateModel(
            name='InsuranceAgentInfo',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='account.user')),
                ('name', models.CharField(max_length=30, null=True)),
                ('licenseNumber', models.CharField(max_length=20, null=True)),
                ('mobileNumber', models.CharField(max_length=10, null=True)),
                ('description', models.TextField(max_length=255, null=True)),
                ('address', models.CharField(max_length=30, null=True)),
                ('tags', models.TextField(max_length=255, null=True)),
                ('activeIndicator', models.CharField(choices=[('Y', 'YES'), ('N', 'NO')], default='N', max_length=1)),
                ('organization', models.CharField(max_length=30, null=True)),
            ],
        ),
    ]