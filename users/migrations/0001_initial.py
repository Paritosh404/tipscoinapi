# Generated by Django 3.0.7 on 2021-05-22 05:51

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='UserData',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=25)),
                ('lastname', models.CharField(max_length=25)),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('provider', models.CharField(blank=True, max_length=25, null=True)),
                ('datetime', models.DateTimeField(auto_now=True)),
                ('phone_no', models.BigIntegerField(null=True, validators=[django.core.validators.MaxValueValidator(99999999999), django.core.validators.MinValueValidator(0)])),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.CreateModel(
            name='UserAlert',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.EmailField(max_length=254)),
                ('coin_name', models.CharField(max_length=25)),
                ('default_alert', models.BooleanField(default=True)),
                ('custom_alert', models.BooleanField(default=False)),
                ('custom_alert_price', models.FloatField(blank=True, null=True)),
                ('custom_alert_percentage', models.FloatField(blank=True, null=True)),
                ('last_send_email', models.DateTimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'UserAlert',
                'verbose_name_plural': 'User Alerts',
                'unique_together': {('user_email', 'coin_name')},
            },
        ),
    ]
