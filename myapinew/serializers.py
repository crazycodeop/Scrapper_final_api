from rest_framework import serializers
from myapinew.models import (
    res_sale_model,
    res_rent_model,
    res_pg_model,
    comm_sale_model,
    comm_lease_model,
    no_broker_rent_model,
    no_broker_sale_model,
    no_broker_comm_rent_model,
    no_broker_comm_sale_model,
    no_broker_pg_model,
)


class resSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = res_sale_model
        fields = '__all__'


class resRentSerializer(serializers.ModelSerializer):
    class Meta:
        model = res_rent_model
        fields = '__all__'


class resPgSerializer(serializers.ModelSerializer):
    class Meta:
        model = res_pg_model
        fields = '__all__'


class commSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = comm_sale_model
        fields = '__all__'


class commLeaseSerializer(serializers.ModelSerializer):
    class Meta:
        model = comm_lease_model
        fields = '__all__'


class noBrokerRentSerializer(serializers.ModelSerializer):
    class Meta:
        model = no_broker_rent_model
        fields = '__all__'


class noBrokerSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = no_broker_sale_model
        fields = '__all__'


class noBrokerCommRentSerializer(serializers.ModelSerializer):
    class Meta:
        model = no_broker_comm_rent_model
        fields = '__all__'


class noBrokerCommSaleSerializer(serializers.ModelSerializer):
    class Meta:
        model = no_broker_comm_sale_model
        fields = '__all__'


class noBrokerPgSerializer(serializers.ModelSerializer):
    class Meta:
        model = no_broker_pg_model
        fields = '__all__'
