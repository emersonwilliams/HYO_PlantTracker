# Generated by Django 3.0.8 on 2020-07-24 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.AutoField(primary_key=True, serialize=False)),
                ('user_name', models.CharField(max_length=30)),
                ('passwd', models.CharField(max_length=30)),
            ],
        ),
    ]
