# Generated by Django 4.2.2 on 2023-07-02 07:23

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('user_id', models.CharField(max_length=33, primary_key=True, serialize=False, unique=True, validators=[django.core.validators.RegexValidator('U[0-9a-f]{32}')])),
                ('name', models.CharField(max_length=100, validators=[django.core.validators.MaxLengthValidator(100)])),
                ('type', models.IntegerField(choices=[(-1, 'deleted'), (0, 'user'), (1, 'admin')])),
                ('status', models.IntegerField(default=0)),
            ],
        ),
    ]
