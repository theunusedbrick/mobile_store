# Generated by Django 2.2.3 on 2020-04-01 18:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_store', '0022_auto_20200401_1855'),
    ]

    operations = [
        migrations.DeleteModel(
            name='PhoneCategory',
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.CharField(choices=[('AP', 'Apple'), ('AN', 'Android')], default='AP', max_length=2),
        ),
    ]
