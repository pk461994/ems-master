# Generated by Django 2.2.7 on 2020-04-18 11:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0009_auto_20181002_1544'),
    ]

    operations = [
        migrations.AlterField(
            model_name='question',
            name='title',
            field=models.TextField(blank=True, null=True),
        ),
    ]
