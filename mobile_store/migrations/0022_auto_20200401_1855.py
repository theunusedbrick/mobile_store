# Generated by Django 2.2.3 on 2020-04-01 17:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_store', '0021_auto_20200401_1827'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PhoneCat',
            new_name='PhoneCategory',
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='mobile_store.Category'),
        ),
    ]
