# Generated by Django 4.1.5 on 2023-01-16 02:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapi', '0002_remove_entries_date_alter_entries_owner'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entries',
            name='owner',
            field=models.CharField(max_length=100),
        ),
    ]