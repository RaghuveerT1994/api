import os
from django.conf import settings
from django.db import models
from django.db.models import Q, fields
from django.contrib.auth.models import User

from rest_framework import serializers

from rule_engine.models import TBLRules, CommonMaster, TBLRulesSet,TBLRuleFunctionsOperation,TBLRulesConfiguration,TBLRulesConfigurationCondition,TBLRulesConfigurationValues,TBLRulesGroup,TBLRulesAudit

class TBLRulesSerializer(serializers.ModelSerializer):   
    # created_user= serializers.SerializerMethodField()
    # updated_user= serializers.SerializerMethodField()

    class Meta:
        model = TBLRules
        fields = ('rules_id', 'rules_name', 'rules_sequence', 'isOpty', 'extras', 'is_deleted', 'isActive',  'created_user', 'created_at', 'updated_user', 'updated_at')

 
class CommonMasterSerializer(serializers.ModelSerializer):   

    class Meta:
        model = CommonMaster
        fields = ('cm_id', 'cm_type', 'cm_name', 'cm_value', 'cm_order')

class TBLRulesSetSerializer(serializers.ModelSerializer):   

    class Meta:
        model = TBLRulesSet
        fields = ('rules_set_id', 'rules_set_name', 'rules_set_sequence', 'rules_id', 'extras', 'is_deleted', 'isActive',  'created_user', 'created_at', 'updated_user', 'updated_at')

class TBLRulesFunctionOperationSerializer(serializers.ModelSerializer):   

    class Meta:
        model = TBLRuleFunctionsOperation
        fields = ('functions_id', 'functions_name', 'isFuntion', 'isOpertion', 'extras', 'is_deleted', 'isActive',  'created_user', 'created_at', 'updated_user', 'updated_at')


class TBLRulesConfigurationsSerializer(serializers.ModelSerializer):   

    class Meta:
        model = TBLRulesConfiguration
        fields = ('rules_config_id', 'rules_config_name', 'rules_set_sequence', 'condition_sequence', 'function_id', 'rules_set_id', 'isUiVisible',  'extras', 'is_deleted','isActive','created_user','created_at', 'updated_user', 'updated_at')

class TBLRulesConfigurationConditionsSerializer(serializers.ModelSerializer):   

    class Meta:
        model = TBLRulesConfigurationCondition
        fields = ('rcc_id', 'isLhs', 'rcc_sequence', 'operation_id', 'rcc_type', 'function_id', 'rules_config_id', 'extras', 'is_deleted','isActive','created_user','created_at', 'updated_user', 'updated_at')

class TBLRulesConfigurationValueSerializer(serializers.ModelSerializer):   

    class Meta:
        model = TBLRulesConfigurationValues
        fields = ('rcv_id', 'rcv_sequence', 'value_type', 'value_display_name', 'value_tooltip', 'value_table_name','value_table_column','value_name', 'rcc_id', 'extras', 'is_deleted','isActive','created_user','created_at', 'updated_user', 'updated_at')

class TBLRulesGroupsSerializer(serializers.ModelSerializer):   

    class Meta:
        model = TBLRulesGroup
        fields = ('rules_group_id', 'rules_config_id', 'parent_group_no', 'group_no', 'rule_set_condition','extras', 'is_deleted','isActive','created_user','created_at', 'updated_user', 'updated_at')

class TBLRulesEngineAuditSerializer(serializers.ModelSerializer):   

    class Meta:
        model = TBLRulesAudit
        fields = ('rules_audit_id', 'rules_config_id', 'rules_group_id', 'field_name', 'old_value', 'new_value','user', 'extras', 'is_deleted','isActive','created_user','created_at', 'updated_user', 'updated_at')
