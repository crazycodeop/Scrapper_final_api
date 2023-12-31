# Generated by Django 4.1.5 on 2023-02-15 18:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapinew', '0004_no_broker_model_nearby'),
    ]

    operations = [
        migrations.CreateModel(
            name='no_broker_sale_model',
            fields=[
                ('Id', models.IntegerField(primary_key=True, serialize=False)),
                ('Date_Posted', models.TextField(null=True)),
                ('Link', models.TextField()),
                ('Price', models.TextField()),
                ('EMI', models.TextField()),
                ('Nearby', models.TextField(null=True)),
                ('SQFT', models.TextField()),
                ('Facing', models.TextField()),
                ('Bathrooms', models.TextField()),
                ('Apt_Type', models.TextField()),
                ('Apt_Name', models.TextField()),
                ('Parking', models.TextField()),
                ('Bedrooms', models.TextField()),
                ('Possesion_By', models.TextField()),
                ('Balcony', models.TextField()),
                ('Power_Backup', models.TextField()),
            ],
        ),
        migrations.RenameModel(
            old_name='no_broker_model',
            new_name='no_broker_rent_model',
        ),
    ]
