# Generated by Django 2.0 on 2018-03-23 23:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SearchedWords',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('word', models.CharField(max_length=310, unique=True)),
                ('hmany', models.IntegerField(default=1)),
            ],
        ),
    ]
