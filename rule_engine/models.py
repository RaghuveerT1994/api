from enum import Enum
from django.db import models
from django.utils import timezone

class TBLRules(models.Model):
    rules_id = models.AutoField(primary_key=True, db_index=True)
    rules_name= models.CharField(max_length=200, blank=True, null=True)
    rules_sequence= models.IntegerField(blank=True, null=True)  
    isOpty= models.BooleanField(default=False, null=True, blank=True)
    extras= models.JSONField(default=dict, blank=True, null=True)
    is_deleted= models.BooleanField(default=False, null=True, blank=True)
    isActive= models.BooleanField(default=False, null=True, blank=True)
    created_user= models.IntegerField(blank=False, null=False)
    created_at= models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_user= models.IntegerField(blank=True, null=True)
    updated_at= models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_rules'

class TBLRulesSet(models.Model):
    rules_set_id = models.AutoField(primary_key=True, db_index=True)
    rules_set_name= models.CharField(max_length=200, blank=True, null=True)
    rules_set_sequence= models.IntegerField(blank=True, null=True)  
    rules_id= models.ForeignKey(TBLRules, db_column='rules_id', on_delete=models.CASCADE, blank=False, null=False)
    extras= models.JSONField(default=dict, blank=True, null=True)
    is_deleted= models.BooleanField(default=False, null=True, blank=True)
    isActive= models.BooleanField(default=False, null=True, blank=True)
    created_user= models.IntegerField(blank=False, null=False)
    created_at= models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_user= models.IntegerField(blank=True, null=True)
    updated_at= models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_rules_set'


class TBLRuleFunctionsOperation(models.Model):
    functions_id = models.AutoField(primary_key=True, db_index=True)
    functions_name= models.CharField(max_length=200, blank=True, null=True)
    isOpertion= models.BooleanField(default=False, null=True, blank=True)
    isFuntion= models.BooleanField(default=False, null=True, blank=True)
    extras= models.JSONField(default=dict, blank=True, null=True)
    is_deleted= models.BooleanField(default=False, null=True, blank=True)
    isActive= models.BooleanField(default=False, null=True, blank=True)
    created_user= models.IntegerField(blank=False, null=False)
    created_at= models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_user= models.IntegerField(blank=True, null=True)
    updated_at= models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_rules_functions_operation'

class TBLRulesConfiguration(models.Model): 
    rules_config_id = models.AutoField(primary_key=True, db_index=True)
    rules_config_name= models.CharField(max_length=200, blank=True, null=True)
    rules_set_sequence= models.IntegerField(blank=True, null=True)  
    condition_sequence= models.IntegerField(blank=True, null=True)  
    function_id = models.ForeignKey(TBLRuleFunctionsOperation, db_column='function_id', on_delete=models.CASCADE, blank=False, null=False)
    rules_set_id= models.ForeignKey(TBLRulesSet, db_column='rules_set_id', on_delete=models.CASCADE, blank=False, null=False)
    isUiVisible= models.BooleanField(default=False, null=True, blank=True)
    extras= models.JSONField(default=dict, blank=True, null=True)
    is_deleted= models.BooleanField(default=False, null=True, blank=True)
    isActive= models.BooleanField(default=False, null=True, blank=True)
    created_user= models.IntegerField(blank=False, null=False)
    created_at= models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_user= models.IntegerField(blank=True, null=True)
    updated_at= models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_rules_configuration'

class TBLRulesConfigurationCondition(models.Model): 
    rcc_id = models.AutoField(primary_key=True, db_index=True)
    isLhs= models.BooleanField(default=False, null=True, blank=True)
    rcc_sequence= models.IntegerField(blank=True, null=True)  
    operation_id = models.ForeignKey(TBLRuleFunctionsOperation, related_name='operation_id', on_delete=models.CASCADE, blank=False, null=False)
    rcc_type= models.IntegerField(blank=True, null=True)  
    function_id = models.ForeignKey(TBLRuleFunctionsOperation, db_column='function_id', on_delete=models.CASCADE, blank=False, null=False)
    rules_config_id = models.ForeignKey(TBLRulesConfiguration, db_column='rules_config_id', on_delete=models.CASCADE, blank=False, null=False)
    extras= models.JSONField(default=dict, blank=True, null=True)
    is_deleted= models.BooleanField(default=False, null=True, blank=True)
    isActive= models.BooleanField(default=False, null=True, blank=True)
    created_user= models.IntegerField(blank=False, null=False)
    created_at= models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_user= models.IntegerField(blank=True, null=True)
    updated_at= models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_rules_configuration_condition'

class TBLRulesConfigurationValues(models.Model): 
    rcv_id = models.AutoField(primary_key=True, db_index=True)
    rcv_sequence= models.IntegerField(blank=True, null=True)  
    value_type= models.IntegerField(blank=True, null=True)  
    value_display_name= models.CharField(max_length=200, blank=True, null=True)
    value_tooltip= models.CharField(max_length=200, blank=True, null=True)
    value_table_name= models.CharField(max_length=200, blank=True, null=True)
    value_table_column= models.CharField(max_length=200, blank=True, null=True)
    value_name= models.CharField(max_length=200, blank=True, null=True)
    rcc_id = models.ForeignKey(TBLRulesConfigurationCondition, db_column='rcc_id', on_delete=models.CASCADE, blank=False, null=False)
    extras= models.JSONField(default=dict, blank=True, null=True)
    is_deleted= models.BooleanField(default=False, null=True, blank=True)
    isActive= models.BooleanField(default=False, null=True, blank=True)
    created_user= models.IntegerField(blank=False, null=False)
    created_at= models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_user= models.IntegerField(blank=True, null=True)
    updated_at= models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_rules_configuration_values'

class TBLRulesGroup(models.Model): 
    rules_group_id = models.AutoField(primary_key=True, db_index=True)
    rules_config_id = models.ForeignKey(TBLRulesConfiguration, db_column='rules_config_id', on_delete=models.CASCADE, blank=False, null=False)
    parent_group_no= models.IntegerField(blank=True, null=True)  
    group_no= models.IntegerField(blank=True, null=True)  
    rule_set_condition= models.CharField(max_length=200, blank=True, null=True)
    extras= models.JSONField(default=dict, blank=True, null=True)
    is_deleted= models.BooleanField(default=False, null=True, blank=True)
    isActive= models.BooleanField(default=False, null=True, blank=True)
    created_user= models.IntegerField(blank=False, null=False)
    created_at= models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_user= models.IntegerField(blank=True, null=True)
    updated_at= models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_rules_group'


class TBLRulesAudit(models.Model): 
    rules_audit_id = models.AutoField(primary_key=True, db_index=True)
    rules_config_id = models.ForeignKey(TBLRulesConfiguration, db_column='rules_config_id', on_delete=models.CASCADE, blank=False, null=False)
    rules_group_id = models.ForeignKey(TBLRulesGroup, db_column='rules_group_id', on_delete=models.CASCADE, blank=False, null=False)
    field_name= models.CharField(max_length=200, blank=True, null=True)
    old_value= models.CharField(max_length=200, blank=True, null=True)
    new_value= models.CharField(max_length=200, blank=True, null=True)
    user= models.CharField(max_length=200, blank=True, null=True)
    extras= models.JSONField(default=dict, blank=True, null=True)
    is_deleted= models.BooleanField(default=False, null=True, blank=True)
    isActive= models.BooleanField(default=False, null=True, blank=True)
    created_user= models.IntegerField(blank=False, null=False)
    created_at= models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_user= models.IntegerField(blank=True, null=True)
    updated_at= models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_rules_audit'


class CommonMaster(models.Model):
    cm_id = models.AutoField(primary_key=True, db_index=True)
    cm_type= models.CharField(max_length=200, blank=True, null=True)
    cm_name= models.CharField(max_length=200, blank=True, null=True)
    cm_value= models.CharField(max_length=200, blank=True, null=True)
    cm_order= models.IntegerField(blank=True, null=True)
    extras= models.JSONField(default=dict, blank=True, null=True)
    is_deleted= models.BooleanField(default=False, null=True, blank=True)
    isActive= models.BooleanField(default=False, null=True, blank=True)
    created_user= models.IntegerField(blank=False, null=False)
    created_at= models.DateTimeField(default=timezone.now, null=True, blank=True)
    updated_user= models.IntegerField(blank=True, null=True)
    updated_at= models.DateTimeField(blank=True, null=True)

    class Meta:
        db_table = 'tbl_common_master'