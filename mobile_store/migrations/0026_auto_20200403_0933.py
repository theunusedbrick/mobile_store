# Generated by Django 2.2.3 on 2020-04-03 08:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_store', '0025_review'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='user',
        ),
        migrations.AddField(
            model_name='review',
            name='name',
            field=models.CharField(default='user', max_length=128),
        ),
    ]
