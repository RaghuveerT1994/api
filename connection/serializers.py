from rest_framework import serializers
from connection.models import ConnectionHistory, ConnectionType, FieldMaster, Connection
from django.contrib.auth.models import User


class ConnectionTypeSerializer(serializers.ModelSerializer):

 class Meta:
    model = ConnectionType
    fields = ('connection_type_id', 'connection_type', 'connection_type_name', 'connection_type_code', 'input_field_id', 'is_source_connection_type', 'is_destination_connection_type', 'application_code')

class ConnectionTypeViewSerializer(serializers.ModelSerializer):

 class Meta:
    model = ConnectionType
    fields = ('connection_type_id', 'connection_type', 'connection_type_name', 'connection_type_code', 'is_source_connection_type', 'is_destination_connection_type', 'application_code')


class FieldMasterSerializer(serializers.ModelSerializer):

 class Meta:
    model = FieldMaster
    fields = ('field_master_id', 'field_label', 'field_type', 'field_data_type', 'field_code', 'max_length',
              'min_length', 'required', 'extras')


class ConnectionSerializer(serializers.ModelSerializer):

 class Meta:
    model = Connection
    fields = ('name', 'description', 'parameter', 'created_by', 'status', 'connection_type_id', 'is_deleted')

class ConnectionViewSerializer(serializers.ModelSerializer):

 class Meta:
    model = Connection
    fields = ('connection_id', 'connection_type_id', 'name', 'description', 'parameter', 'status', 'created_by', 'created_date', 'updated_by', 'updated_date')

class ConnectionListSerializer(serializers.ModelSerializer):
    status= serializers.CharField(source='get_status_display')
    connection_type= serializers.CharField(source='connection_type_id.connection_type', default='', read_only=True)
    connection_type_name= serializers.CharField(source='connection_type_id.connection_type_name', default='', read_only=True)
    connection_type_code= serializers.CharField(source='connection_type_id.connection_type_code', default='', read_only=True)
    description = serializers.CharField(source='connection_type_id.connection_type_description', default='', read_only=True)
    is_source_connection_type= serializers.CharField(source='connection_type_id.is_source_connection_type', default='', read_only=True)
    is_destination_connection_type= serializers.CharField(source='connection_type_id.is_destination_connection_type', default='', read_only=True)
    application_code= serializers.CharField(source='connection_type_id.application_code', default='', read_only=True)
    created_user= serializers.SerializerMethodField()
    updated_user= serializers.SerializerMethodField()

    class Meta:
        model = Connection
        fields = ('connection_id', 'name', 'description', 'parameter', 'created_date', 'updated_date', 'created_by', 'updated_by', 'status', 'connection_type_id', 'connection_type','connection_type_name','connection_type_code','is_source_connection_type', 'is_destination_connection_type', 'application_code', 'created_user', 'updated_user')

    def get_created_user(self, obj):
        current_values =User.objects.get(id=obj.created_by)
        if current_values:
            return current_values.first_name+ " " +current_values.last_name
        else:
            return ''
            
    def get_updated_user(self, obj):
        if obj.updated_by:
            current_values =User.objects.get(id=obj.updated_by)
            if current_values:
                return current_values.first_name+ " " +current_values.last_name
            else:
                return ''
        else:
            return ''

class ConnectionHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ConnectionHistory

        fields = ('connection_history_id', 'connection_id', 'changed_attributes', 'table_name', 'history_status', 'description', 'created_by', 'created_date')
      
class ConnectionHistoryListSerializer(serializers.ModelSerializer):
    created_user= serializers.SerializerMethodField()
    class Meta:
        model = ConnectionHistory

        fields = ('connection_history_id', 'connection_id', 'table_name', 'history_status', 'description', 'created_by', 'created_date', 'updated_by', 'updated_date', 'created_user')

    def get_created_user(self, obj):
        current_values =User.objects.get(id=obj.created_by)
        if current_values:
            return current_values.first_name+ " "+current_values.last_name
        else:
            return ''

class ConnectionCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Connection
        fields = ('connection_type_id', 'parameter')

class ListSerializer(serializers.Serializer):
    limit = serializers.IntegerField(default=10, help_text='query limit')
    offset = serializers.IntegerField(default=0, help_text='query offset')

class ConnectionUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = Connection
        fields = ('name', 'description', 'parameter', 'connection_type_id', 'parameter', 'status')

class ConnectionHistorySerializer(serializers.ModelSerializer):

    class Meta:
        model = ConnectionHistory
        fields = ('connection_id',)
