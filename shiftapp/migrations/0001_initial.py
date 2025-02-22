# Generated by Django 3.0.5 on 2020-05-20 01:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ShiftBaseModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('check', models.BooleanField()),
                ('duty', models.CharField(max_length=10)),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('two', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='ShiftModel',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.IntegerField()),
                ('year', models.IntegerField()),
                ('month', models.IntegerField()),
                ('base_id', models.IntegerField()),
            ],
        ),
    ]
