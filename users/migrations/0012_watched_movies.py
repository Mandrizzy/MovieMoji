# Generated by Django 2.1.5 on 2019-05-20 02:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0011_auto_20190519_1653'),
    ]

    operations = [
        migrations.CreateModel(
            name='watched_movies',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
    ]