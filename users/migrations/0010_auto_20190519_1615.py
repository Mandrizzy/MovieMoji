# Generated by Django 2.2 on 2019-05-19 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0009_auto_20190519_1614'),
    ]

    operations = [
        migrations.AlterModelTable(
            name='movies',
            table='users_movies',
        ),
    ]
