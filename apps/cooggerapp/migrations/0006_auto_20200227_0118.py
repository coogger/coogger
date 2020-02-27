# Generated by Django 3.0.3 on 2020-02-27 07:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cooggerapp', '0005_utopic_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commit',
            name='body',
            field=models.TextField(),
        ),
        migrations.AlterField(
            model_name='content',
            name='body',
            field=models.TextField(help_text='Your content | problem | question | or anything else', verbose_name=''),
        ),
        migrations.AlterField(
            model_name='issue',
            name='body',
            field=models.TextField(blank=True, help_text='Your problem | question | or anything else', null=True),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='about',
            field=models.TextField(blank=True, help_text='Write a long article about yourself, see; /u/@your_username/about/', null=True, verbose_name='About Yourself'),
        ),
    ]
