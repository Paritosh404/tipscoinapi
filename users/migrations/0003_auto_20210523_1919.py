# Generated by Django 3.0.7 on 2021-05-23 13:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_coinsuggestion'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coinsuggestion',
            name='user_email',
            field=models.EmailField(blank=True, max_length=254, null=True),
        ),
    ]
