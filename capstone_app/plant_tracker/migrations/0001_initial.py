# Generated by Django 3.0.8 on 2020-07-16 00:56

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Example',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rand_attr', models.CharField(max_length=12)),
            ],
        ),
    ]