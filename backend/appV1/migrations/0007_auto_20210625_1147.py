# Generated by Django 3.2.2 on 2021-06-25 06:17

import datetime
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('appV1', '0006_personalinfo_profilepicture'),
    ]

    operations = [
        migrations.AlterField(
            model_name='personalinfo',
            name='profilePicture',
            field=models.ImageField(null=True, upload_to='profile_pictures/'),
        ),
        migrations.CreateModel(
            name='LabReportInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20, null=True)),
                ('report', models.FileField(null=True, upload_to='labreports/')),
                ('tag', models.CharField(max_length=20, null=True)),
                ('report_status', models.CharField(max_length=20, null=True)),
                ('created_on', models.DateField(default=datetime.date.today)),
                ('userId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
