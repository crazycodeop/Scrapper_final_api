from django.db import models


class res_sale_model(models.Model):
    Id = models.AutoField(primary_key=True)
    Date_Posted = models.TextField(null=True, blank=True)
    Proptype = models.TextField(null=True, blank=True)
    Link = models.TextField(null=True, blank=True)
    Owner = models.TextField(null=True, blank=True)
    BHK = models.TextField(null=True, blank=True)
    Locality = models.TextField(null=True, blank=True)
    City = models.TextField(null=True, blank=True)
    Price = models.TextField(null=True, blank=True)
    Carpet_Area = models.TextField(null=True, blank=True)
    Furnishing = models.TextField(null=True, blank=True)
    Bathrooms = models.TextField(null=True, blank=True)
    Facing = models.TextField(null=True, blank=True)
    Status = models.TextField(null=True, blank=True)
    Transaction = models.TextField(null=True, blank=True)
    Price_Sqft = models.TextField(null=True, blank=True)
    Floor = models.TextField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "MagicBricks Residential Sale"
        verbose_name_plural = "MagicBricks Residential Sales"

    def __str__(self):
        return f"{self.BHK or ''} {self.Proptype or ''} - {self.Locality or self.City or 'Sale'}"


class res_rent_model(models.Model):
    Id = models.AutoField(primary_key=True)
    Date_Posted = models.TextField(null=True, blank=True)
    Proptype = models.TextField(null=True, blank=True)
    Link = models.TextField(null=True, blank=True)
    Owner = models.TextField(null=True, blank=True)
    BHK = models.TextField(null=True, blank=True)
    Locality = models.TextField(null=True, blank=True)
    City = models.TextField(null=True, blank=True)
    Rent = models.TextField(null=True, blank=True)
    Carpet_Area = models.TextField(null=True, blank=True)
    Furnishing = models.TextField(null=True, blank=True)
    Facing = models.TextField(null=True, blank=True)
    Tenant = models.TextField(null=True, blank=True)
    Floor = models.TextField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "MagicBricks Residential Rent"
        verbose_name_plural = "MagicBricks Residential Rents"

    def __str__(self):
        return f"{self.BHK or ''} {self.Proptype or ''} - {self.Locality or self.City or 'Rent'}"


class res_pg_model(models.Model):
    Id = models.AutoField(primary_key=True)
    Posted_by = models.TextField(null=True, blank=True)
    Proptype = models.TextField(null=True, blank=True)
    Link = models.TextField(null=True, blank=True)
    Owner = models.TextField(null=True, blank=True)
    Locality = models.TextField(null=True, blank=True)
    City = models.TextField(null=True, blank=True)
    Charges = models.TextField(null=True, blank=True)
    PG_for = models.TextField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "MagicBricks PG"
        verbose_name_plural = "MagicBricks PGs"

    def __str__(self):
        return f"{self.Owner or self.PG_for or 'PG'} - {self.Locality or self.City or ''}"


class comm_sale_model(models.Model):
    Id = models.AutoField(primary_key=True)
    Date_Posted = models.TextField(null=True, blank=True)
    Proptype = models.TextField(null=True, blank=True)
    Link = models.TextField(null=True, blank=True)
    Owner = models.TextField(null=True, blank=True)
    Locality = models.TextField(null=True, blank=True)
    City = models.TextField(null=True, blank=True)
    Price = models.TextField(null=True, blank=True)
    Carpet_Area = models.TextField(null=True, blank=True)
    Parking = models.TextField(null=True, blank=True)
    Property_Age = models.TextField(null=True, blank=True)
    Facing = models.TextField(null=True, blank=True)
    Water_Availability = models.TextField(null=True, blank=True)
    Pantry = models.TextField(null=True, blank=True)
    Overlooking = models.TextField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "MagicBricks Commercial Sale"
        verbose_name_plural = "MagicBricks Commercial Sales"

    def __str__(self):
        return f"{self.Proptype or 'Commercial Sale'} - {self.Locality or self.City or ''}"


class comm_lease_model(models.Model):
    Id = models.AutoField(primary_key=True)
    Date_Posted = models.TextField(null=True, blank=True)
    Proptype = models.TextField(null=True, blank=True)
    Link = models.TextField(null=True, blank=True)
    Retailer = models.TextField(null=True, blank=True)
    BHK = models.TextField(null=True, blank=True)
    Locality = models.TextField(null=True, blank=True)
    City = models.TextField(null=True, blank=True)
    Price = models.TextField(null=True, blank=True)
    Carpet_Area = models.TextField(null=True, blank=True)
    Washroom = models.TextField(null=True, blank=True)
    Facing = models.TextField(null=True, blank=True)
    Pantry = models.TextField(null=True, blank=True)
    Parking = models.TextField(null=True, blank=True)
    Water_Availability = models.TextField(null=True, blank=True)
    Price_Sqft = models.TextField(null=True, blank=True)
    Property_Age = models.TextField(null=True, blank=True)
    Description = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "MagicBricks Commercial Lease"
        verbose_name_plural = "MagicBricks Commercial Leases"

    def __str__(self):
        return f"{self.Retailer or 'Commercial Lease'} - {self.Locality or self.City or ''}"


class no_broker_rent_model(models.Model):
    Id = models.AutoField(primary_key=True)
    Date_Posted = models.TextField(null=True, blank=True)
    Link = models.TextField(null=True, blank=True)
    Rent = models.TextField(null=True, blank=True)
    EMI = models.TextField(null=True, blank=True)
    Nearby = models.TextField(null=True, blank=True)
    SQFT = models.TextField(null=True, blank=True)
    Furnishing = models.TextField(null=True, blank=True)
    Available_from = models.TextField(null=True, blank=True)
    Prop_Type = models.TextField(null=True, blank=True)
    Preferred_Tenants = models.TextField(null=True, blank=True)
    Apt_Type = models.TextField(null=True, blank=True)
    Parking = models.TextField(null=True, blank=True)
    Bedrooms = models.TextField(null=True, blank=True)
    Possesion_By = models.TextField(null=True, blank=True)
    Balcony = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "NoBroker Rent"
        verbose_name_plural = "NoBroker Rents"

    def __str__(self):
        return f"{self.Apt_Type or 'Rent'} - {self.Nearby or 'Property'}"


class no_broker_sale_model(models.Model):
    Id = models.AutoField(primary_key=True)
    Date_Posted = models.TextField(null=True, blank=True)
    Link = models.TextField(null=True, blank=True)
    Price = models.TextField(null=True, blank=True)
    EMI = models.TextField(null=True, blank=True)
    Nearby = models.TextField(null=True, blank=True)
    SQFT = models.TextField(null=True, blank=True)
    Facing = models.TextField(null=True, blank=True)
    Bathrooms = models.TextField(null=True, blank=True)
    Apt_Type = models.TextField(null=True, blank=True)
    Apt_Name = models.TextField(null=True, blank=True)
    Parking = models.TextField(null=True, blank=True)
    Bedrooms = models.TextField(null=True, blank=True)
    Possesion_By = models.TextField(null=True, blank=True)
    Balcony = models.TextField(null=True, blank=True)
    Power_Backup = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "NoBroker Sale"
        verbose_name_plural = "NoBroker Sales"

    def __str__(self):
        return f"{self.Apt_Type or 'Sale'} - {self.Apt_Name or self.Nearby or 'Property'}"


class no_broker_comm_rent_model(models.Model):
    Id = models.AutoField(primary_key=True)
    Date_Posted = models.TextField(null=True, blank=True)
    Link = models.TextField(null=True, blank=True)
    Rent = models.TextField(null=True, blank=True)
    Deposit = models.TextField(null=True, blank=True)
    Nearby = models.TextField(null=True, blank=True)
    SQFT = models.TextField(null=True, blank=True)
    Floor = models.TextField(null=True, blank=True)
    Prop_Type = models.TextField(null=True, blank=True)
    Furnishing = models.TextField(null=True, blank=True)
    Availability = models.TextField(null=True, blank=True)
    Parking = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "NoBroker Commercial Rent"
        verbose_name_plural = "NoBroker Commercial Rents"

    def __str__(self):
        return f"{self.Prop_Type or 'Comm Rent'} - {self.Nearby or 'Property'}"


class no_broker_comm_sale_model(models.Model):
    Id = models.AutoField(primary_key=True)
    Date_Posted = models.TextField(null=True, blank=True)
    Link = models.TextField(null=True, blank=True)
    Price = models.TextField(null=True, blank=True)
    EMI = models.TextField(null=True, blank=True)
    Nearby = models.TextField(null=True, blank=True)
    SQFT = models.TextField(null=True, blank=True)
    Facing = models.TextField(null=True, blank=True)
    Bathrooms = models.TextField(null=True, blank=True)
    Apt_Type = models.TextField(null=True, blank=True)
    Parking = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "NoBroker Commercial Sale"
        verbose_name_plural = "NoBroker Commercial Sales"

    def __str__(self):
        return f"{self.Apt_Type or 'Comm Sale'} - {self.Nearby or 'Property'}"


class no_broker_pg_model(models.Model):
    Id = models.AutoField(primary_key=True)
    Date_Posted = models.TextField(null=True, blank=True)
    Link = models.TextField(null=True, blank=True)
    Rent = models.TextField(null=True, blank=True)
    Deposit = models.TextField(null=True, blank=True)
    Nearby = models.TextField(null=True, blank=True)
    Room_Type = models.TextField(null=True, blank=True)
    Preferred_Tenants = models.TextField(null=True, blank=True)
    Food = models.TextField(null=True, blank=True)
    Parking = models.TextField(null=True, blank=True)
    Possesion_By = models.TextField(null=True, blank=True)

    class Meta:
        verbose_name = "NoBroker PG"
        verbose_name_plural = "NoBroker PGs"

    def __str__(self):
        return f"{self.Room_Type or 'PG'} - {self.Nearby or 'Property'}"
