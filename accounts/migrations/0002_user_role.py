# Generated by Django 4.2.11 on 2024-03-22 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='role',
            field=models.CharField(choices=[('admin', 'Admin'), ('assistant', 'Assistant'), ('user', 'User')], default='user', max_length=20, verbose_name='role'),
        ),
    ]
