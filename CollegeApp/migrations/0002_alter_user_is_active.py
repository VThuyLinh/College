# Generated by Django 4.2.21 on 2025-05-29 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CollegeApp', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='is_active',
            field=models.BooleanField(default=1, verbose_name='Tình trạng tài khoản'),
        ),
    ]
