# Generated by Django 2.2.7 on 2020-04-19 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('poll', '0010_auto_20200418_1658'),
    ]

    operations = [
        migrations.AddField(
            model_name='choice',
            name='is_answer',
            field=models.BooleanField(default=False),
        ),
    ]