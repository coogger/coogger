# Generated by Django 2.0 on 2018-06-26 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('cooggerapp', '0018_auto_20180626_1913'),
    ]

    operations = [
        migrations.RenameField(
            model_name='content',
            old_name='content_list',
            new_name='topic',
        ),
    ]
