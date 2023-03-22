from enum import Enum

""" Import Django libraries """
from django.db import models
from django.utils import timezone


class StatusEnum(Enum):
    Active= 1
    Inactive= 2
    Draft= 3
    New= 4
    Running= 5
    Pause= 6
    Stopped= 7
    Failed= 8

    @classmethod
    def choices(cls):
        return [(key.value, key.name) for key in cls]

class FieldMaster(models.Model):
    """Field Master Model
    This model will have all connection type and its details.
    This data will be used to show the available connection that can be configure

    Model Type: Parent Table
    Depend ON: NA
    Table Name:field_master
    """
    field_master_id = models.AutoField(primary_key=True, db_index=True)
    field_label= models.CharField(max_length=300, blank=False, null=False)
    field_type= models.CharField(max_length=300, blank=False, null=False)
    field_data_type= models.CharField(max_length=300, blank=True, null=True)
    field_code= models.CharField(max_length=300, blank=False, null=False)
    backend_code= models.CharField(max_length=300, blank=True, null=True)
    max_length= models.IntegerField(default=100, null=True, blank=True)
    min_length= models.IntegerField(default=1, null=True, blank=True)
    required= models.BooleanField(default=True, null=True, blank=True)
    extras= models.JSONField(default=dict, blank=True, null=True)
    status = models.IntegerField(choices=StatusEnum.choices(), default=StatusEnum.Active, blank=True, null=True)
    created_by = models.IntegerField(blank=False, null=False)
    created_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'field_master'

class ConnectionType(models.Model):
    """Connection Type model
    This model will have all connection type and its details.
    This data will be used to show the available connection that can be configure

    Model Type: Child Table
    Depend ON: ConnectionField
    Table Name:connection_type
    """
    connection_type_id= models.AutoField(primary_key=True, db_index=True)
    connection_type= models.CharField(max_length=300, blank=False, null=False)
    connection_type_name= models.CharField(max_length=300, blank=False, null=False)
    connection_type_code= models.CharField(max_length=300, blank=False, null=False)
    connection_type_description= models.CharField(max_length=500, blank=False, null=False)
    is_source_connection_type= models.BooleanField(default=True, null=True, blank=True)
    is_destination_connection_type= models.BooleanField(default=True, null=True, blank=True)
    application_code= models.CharField(max_length=300, blank=False, null=False)
    input_field_id= models.JSONField(default=dict, blank=False, null=False)
    output_field_id= models.JSONField(default=dict, blank=False, null=False)
    status= models.IntegerField(choices=StatusEnum.choices(), default=StatusEnum.Active, blank=True, null=True)
    created_by= models.IntegerField(blank=False, null=False)
    created_date= models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_by= models.IntegerField(blank=True, null=True)
    updated_date= models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'connection_type'


class Connection(models.Model):
    """Connection model
    This model will have all connection type and its details.
    This data will be used to show the available connection that can be configure

    Model Type: Child Table
    Depend ON: ConnectionType
    Table Name: connection
    """
    connection_id = models.AutoField(primary_key=True, db_index=True)
    connection_type_id = models.ForeignKey(ConnectionType, db_column='connection_type_id', on_delete=models.CASCADE, blank=False, null=False)
    name= models.CharField(max_length=300, blank=False, null=False)
    description= models.CharField(max_length=500, blank=True, null=True)
    parameter= models.JSONField(default=dict, blank=False, null=False)
    is_deleted= models.BooleanField(default=True, null=True, blank=True)
    status = models.IntegerField(choices=StatusEnum.choices(), default=StatusEnum.Active, blank=True, null=True)
    created_by = models.IntegerField(blank=False, null=False)
    created_date = models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_by = models.IntegerField(blank=True, null=True)
    updated_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'connection'

class ConnectionHistory(models.Model):
    """Connection History model
    This model will have Connection History details

    Model Type: Parent Table
    Depend ON: Connection
    Table Name: connection_history
    """
    connection_history_id= models.AutoField(primary_key=True, db_index=True)
    connection_id= models.ForeignKey(Connection, db_column='connection_id', on_delete=models.CASCADE, blank=False, null=False)
    changed_attributes = models.JSONField(default=dict, blank=True, null=True)
    table_name = models.CharField(max_length=500, blank=True, null=True)
    description = models.CharField(max_length=1000, blank=True, null=True)
    history_status = models.CharField(max_length=100, blank=True, null=True)
    created_by= models.IntegerField(blank=False, null=False)
    created_date= models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_by= models.IntegerField(blank=True, null=True)
    updated_date= models.DateTimeField(blank=True, null=True)
   
    class Meta:
        db_table = 'connection_history'

