# Generated by Django 2.0 on 2018-06-19 22:10

from django.db import migrations, models
import djmd.models


class Migration(migrations.Migration):

    dependencies = [
        ('cooggerapp', '0014_auto_20180505_1415'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content',
            name='approved',
        ),
        migrations.AddField(
            model_name='content',
            name='type',
            field=models.CharField(choices=[('information-sharing', 'information sharing'), ('tutorial-content', 'tutorial content'), ('translation', 'translation'), ('discussion', 'discussion')], default='', max_length=30, verbose_name="content's type"),
        ),
        migrations.AlterField(
            model_name='content',
            name='content',
            field=djmd.models.EditorMdField(),
        ),
        migrations.AlterField(
            model_name='otherinformationofusers',
            name='about',
            field=djmd.models.EditorMdField(),
        ),
    ]
