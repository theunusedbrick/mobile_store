# Generated by Django 2.2.3 on 2020-03-30 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('mobile_store', '0004_auto_20200214_1245'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=128)),
                ('surname', models.CharField(max_length=128)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('feedback', models.CharField(blank=True, max_length=200)),
            ],
        ),
    ]
