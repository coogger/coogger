# Generated by Django 2.0 on 2018-04-18 17:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooggerapp', '0009_auto_20180412_2341'),
    ]

    operations = [
        migrations.AddField(
            model_name='content',
            name='modcomment',
            field=models.BooleanField(default=True, verbose_name='was it comment by mod'),
        ),
        migrations.AlterField(
            model_name='content',
            name='content',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='content',
            name='content_list',
            field=models.CharField(help_text='Please, write your topic about your contents.', max_length=30, verbose_name='title of list'),
        ),
        migrations.AlterField(
            model_name='otherinformationofusers',
            name='about',
            field=models.TextField(),
        ),
    ]
