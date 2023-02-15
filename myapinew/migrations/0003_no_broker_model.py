# Generated by Django 4.1.5 on 2023-02-15 18:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('myapinew', '0002_remove_comm_sale_model_price_sqft_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='no_broker_model',
            fields=[
                ('Id', models.IntegerField(primary_key=True, serialize=False)),
                ('Date_Posted', models.TextField(null=True)),
                ('Link', models.TextField()),
                ('Rent', models.TextField()),
                ('EMI', models.TextField()),
                ('SQFT', models.TextField()),
                ('Furnishing', models.TextField()),
                ('Available_from', models.TextField()),
                ('Prop_Type', models.TextField()),
                ('Preferred_Tenants', models.TextField()),
                ('Apt_Type', models.TextField()),
                ('Parking', models.TextField()),
                ('Bedrooms', models.TextField()),
                ('Possesion_By', models.TextField()),
                ('Balcony', models.TextField()),
            ],
        ),
    ]
