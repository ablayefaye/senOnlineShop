# Generated by Django 3.2.3 on 2021-06-07 17:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('database', '0006_alter_user_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='trash',
            field=models.BooleanField(default=False),
        ),
    ]