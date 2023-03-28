from rest_framework.response import Response
from rest_framework import status
import datetime
from django.contrib.auth.hashers import make_password
import re
from rule_engine.models import TBLRulesConfiguration


import logging
import datetime

log = logging.getLogger(__name__)
pattern = "\W"


class CommonController():

    def ruleConfigurationsInsertDetails(self,request):
        try:
            log.info("ApiCallController api updateDetails")
            insert_data = {}
            if "rules_config_name" not in request.data or not request.data['rules_config_name']:
                return Response({"error": True, "message": "Rules Configuration name is required", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            
            if "rules_config_name" in request.data and request.data['rules_config_name']:
                model_name = TBLRulesConfiguration.objects.filter(rules_config_name=request.data['rules_config_name'].strip())
                if model_name: 
                    return Response( {"error": True, "message": "Rules Configuration name already exists ", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            insert_data["rules_config_name"] = request.data['rules_config_name']
            if "rules_set_sequence" in request.data and request.data['rules_set_sequence']:
                insert_data['rules_set_sequence'] = request.data['rules_set_sequence']
            else:
                {"error": True, "message": "Rules set of sequence name is required", "status": 400}
            if "condition_sequence" in request.data and request.data['condition_sequence']:
                insert_data['condition_sequence'] = request.data['condition_sequence']
            else:
                {"error": True, "message": "Rules condition_sequence name is required", "status": 400}

            if "function_id" in request.data and request.data['function_id']:
                insert_data['function_id'] = request.data['function_id']
            else:
                return {"error": True, "message": "Rules function_id is required", "status": 400}

            if "rules_set_id" in request.data and request.data['rules_set_id']:
                insert_data['rules_set_id'] = request.data['rules_set_id']
            else:
                return {"error": True, "message": "Rules set_id is required", "status": 400}
            
            if "isUiVisible" in request.data and request.data['isUiVisible']:
                insert_data['isUiVisible'] = request.data['isUiVisible']
            else:
                return {"error": True, "message": "Rules isUiVisible is required", "status": 400}

            if "extras" in request.data and request.data['extras']:
                insert_data['extras'] = request.data['extras']
            # else:
            #     return {"error": True, "message": "Rules extras is required", "status": 400}

            if "is_deleted" in request.data and request.data['is_deleted']:
                insert_data['is_deleted'] = request.data['is_deleted']
            else:
                return {"error": True, "message": "Rules is_deleted is required", "status": 400}

            if "isActive" in request.data and request.data['isActive']:
                insert_data['isActive'] = request.data['isActive']
            else:
                return {"error": True, "message": "Rules isActive is required", "status": 400}
            if "created_user" in request.data and request.data['created_user']:
                insert_data['created_user'] = request.data['created_user']
            else:
                return {"error": True, "message": "Rules created_user is required", "status": 400}
            insert_data['created_at'] = request.data['created_at']
            if "updated_user" in request.data and request.data['updated_user']:
                insert_data['updated_user'] = request.data['updated_user']
            else:
                return {"error": True, "message": "Rules updated_user is required", "status": 400}

            insert_data['updated_at'] = datetime.datetime.now()
            
            return insert_data
        except Exception as ex:
            log.info(ex)
            return Response({"error": True, "message": f"we would like to inform you {ex}", "status": 400}, status=status.HTTP_400_BAD_REQUEST)




    def ruleConfigurationConditionInsertDetails(self,request):
        try:
            log.info("ApiCallController api updateDetails")
            insert_data = {}
            if "rules_config_id" not in request.data or not request.data['rules_config_id']:
                return Response({"error": True, "message": "Rules Configuration id is required", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            insert_data["rules_config_id"] = request.data['rules_config_id']
            if "isLhs" in request.data and request.data['isLhs']:
                insert_data['isLhs'] = request.data['isLhs']
            else:
                {"error": True, "message": "Rules Configuration condition isLhs is required", "status": 400}
            if "rcc_sequence" in request.data and request.data['rcc_sequence']:
                insert_data['rcc_sequence'] = request.data['rcc_sequence']
            else:
                {"error": True, "message": "Rules rcc_sequence name is required", "status": 400}

            if "function_id" in request.data and request.data['function_id']:
                insert_data['function_id'] = request.data['function_id']
            else:
                return {"error": True, "message": "Rules function_id is required", "status": 400}

            if "operation_id" in request.data and request.data['operation_id']:
                insert_data['operation_id'] = request.data['operation_id']
            else:
                return {"error": True, "message": "Rules operation_id is required", "status": 400}
            
            if "rcc_type" in request.data and request.data['rcc_type']:
                insert_data['rcc_type'] = request.data['rcc_type']
            else:
                return {"error": True, "message": "Rules rcc_type is required", "status": 400}

            if "extras" in request.data and request.data['extras']:
                insert_data['extras'] = request.data['extras']
            # else:
            #     return {"error": True, "message": "Rules extras is required", "status": 400}

            if "is_deleted" in request.data and request.data['is_deleted']:
                insert_data['is_deleted'] = request.data['is_deleted']
            else:
                return {"error": True, "message": "Rules is_deleted is required", "status": 400}

            if "isActive" in request.data and request.data['isActive']:
                insert_data['isActive'] = request.data['isActive']
            else:
                return {"error": True, "message": "Rules isActive is required", "status": 400}
            if "created_user" in request.data and request.data['created_user']:
                insert_data['created_user'] = request.data['created_user']
            else:
                return {"error": True, "message": "Rules created_user is required", "status": 400}
            insert_data['created_at'] = datetime.datetime.now()
            # else:
            #     return {"error": True, "message": "Rules created_at is required", "status": 400}
            if "updated_user" in request.data and request.data['updated_user']:
                insert_data['updated_user'] = request.data['updated_user']
            else:
                return {"error": True, "message": "Rules updated_user is required", "status": 400}

            insert_data['updated_at'] = datetime.datetime.now()
            # else:
            #     return {"error": True, "message": "Rules updated_at is required", "status": 400}
            return insert_data
        except Exception as ex:
            log.info(ex)
            return Response({"error": True, "message": f"we would like to inform you {ex}", "status": 400}, status=status.HTTP_400_BAD_REQUEST)


    def ruleConfigurationValueInsertDetails(self,request):
        try:
            log.info("ApiCallController api updateDetails")
            insert_data = {}
            if "rcc_id" not in request.data or not request.data['rcc_id']:
                return Response({"error": True, "message": "Rules Configuration id is required", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            if "rcv_sequence" in request.data and request.data['rcv_sequence']:
                insert_data["rcv_sequence"] = request.data['rcv_sequence']
            else:
                {"error": True, "message": "Rules Configuration condition rcv_sequence is required", "status": 400}

            if "value_type" in request.data and request.data['value_type']:
                insert_data['value_type'] = request.data['value_type']
            else:
                {"error": True, "message": "Rules Configuration condition isLhs is required", "status": 400}
            if "value_display_name" in request.data and request.data['value_display_name']:
                insert_data['value_display_name'] = request.data['value_display_name']
            else:
                {"error": True, "message": "Rules value_display_name name is required", "status": 400}

            if "value_tooltip" in request.data and request.data['value_tooltip']:
                insert_data['value_tooltip'] = request.data['value_tooltip']
            else:
                return {"error": True, "message": "Rules value_tooltip is required", "status": 400}

            if "value_table_name" in request.data and request.data['value_table_name']:
                insert_data['value_table_name'] = request.data['value_table_name']
            else:
                return {"error": True, "message": "Rules value_table_name is required", "status": 400}
            
            if "value_table_column" in request.data and request.data['value_table_column']:
                insert_data['value_table_column'] = request.data['value_table_column']
            else:
                return {"error": True, "message": "Rules value_table_column is required", "status": 400}
            
            if "value_name" in request.data and request.data['value_name']:
                insert_data['value_name'] = request.data['value_name']
            else:
                return {"error": True, "message": "Rules value_name is required", "status": 400}
            
            if "rcc_id" in request.data and request.data['rcc_id']:
                insert_data['rcc_id'] = request.data['rcc_id']
            else:
                return {"error": True, "message": "Rules rcc_id is required", "status": 400}
           
            if "extras" in request.data and request.data['extras']:
                insert_data['extras'] = request.data['extras']
            # else:
            #     return {"error": True, "message": "Rules extras is required", "status": 400}

            if "is_deleted" in request.data and request.data['is_deleted']:
                insert_data['is_deleted'] = request.data['is_deleted']
            else:
                return {"error": True, "message": "Rules is_deleted is required", "status": 400}

            if "isActive" in request.data and request.data['isActive']:
                insert_data['isActive'] = request.data['isActive']
            else:
                return {"error": True, "message": "Rules isActive is required", "status": 400}
            if "created_user" in request.data and request.data['created_user']:
                insert_data['created_user'] = request.data['created_user']
            else:
                return {"error": True, "message": "Rules created_user is required", "status": 400}
            insert_data['created_at'] = datetime.datetime.now()
            # else:
            #     return {"error": True, "message": "Rules created_at is required", "status": 400}
            if "updated_user" in request.data and request.data['updated_user']:
                insert_data['updated_user'] = request.data['updated_user']
            else:
                return {"error": True, "message": "Rules updated_user is required", "status": 400}

            insert_data['updated_at'] = datetime.datetime.now()
            # else:
            #     return {"error": True, "message": "Rules updated_at is required", "status": 400}
            return insert_data
        except Exception as ex:
            log.info(ex)
            return Response({"error": True, "message": f"we would like to inform you {ex}", "status": 400}, status=status.HTTP_400_BAD_REQUEST)


    def ruleGroupInsertDetails(self,request):
        try:
            log.info("ApiCallController api updateDetails")
            insert_data = {}
            if "rules_config_id" not in request.data or not request.data['rules_config_id']:
                return Response({"error": True, "message": "Rules Configuration id is required", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
           
            insert_data["rules_config_id"] = request.data['rules_config_id']

            if "parent_group_no" in request.data and request.data['parent_group_no']:
                insert_data['parent_group_no'] = request.data['parent_group_no']
            else:
                {"error": True, "message": "Rules Configuration condition parent_group_no is required", "status": 400}
            if "group_no" in request.data and request.data['group_no']:
                insert_data['group_no'] = request.data['group_no']
            else:
                {"error": True, "message": "Rules group_no name is required", "status": 400}

            if "rule_set_condition" in request.data and request.data['rule_set_condition']:
                insert_data['rule_set_condition'] = request.data['rule_set_condition']
            else:
                return {"error": True, "message": "Rules rule_set_condition is required", "status": 400}

            if "extras" in request.data and request.data['extras']:
                insert_data['extras'] = request.data['extras']
            # else:
            #     return {"error": True, "message": "Rules extras is required", "status": 400}

            if "is_deleted" in request.data and request.data['is_deleted']:
                insert_data['is_deleted'] = request.data['is_deleted']
            else:
                return {"error": True, "message": "Rules is_deleted is required", "status": 400}

            if "isActive" in request.data and request.data['isActive']:
                insert_data['isActive'] = request.data['isActive']
            else:
                return {"error": True, "message": "Rules isActive is required", "status": 400}
            if "created_user" in request.data and request.data['created_user']:
                insert_data['created_user'] = request.data['created_user']
            else:
                return {"error": True, "message": "Rules created_user is required", "status": 400}
            insert_data['created_at'] = datetime.datetime.now()
          
            if "updated_user" in request.data and request.data['updated_user']:
                insert_data['updated_user'] = request.data['updated_user']
            else:
                return {"error": True, "message": "Rules updated_user is required", "status": 400}

            insert_data['updated_at'] = datetime.datetime.now()
       
            return insert_data
        except Exception as ex:
            log.info(ex)
            return Response({"error": True, "message": f"we would like to inform you {ex}", "status": 400}, status=status.HTTP_400_BAD_REQUEST)



    def ruleFunctionalOperationsDetails(self,request):
        try:
            log.info("ApiCallController api updateDetails")
            new_data={}
            if request.data:
                if 'functions_name' in request.data and request.data['functions_name']:
                    new_data['functions_name'] = request.data['functions_name']
                # else:
                #     return {"error": True, "message": "please provide first_name", "status": 400}
                if 'isOperation' in request.data and request.data['isOperation']:
                    new_data['isOperation'] = request.data['isOperation']
                # else:
                #     return {"error": True, "message": "please provide last_name", "status": 400}
                if 'isFunction' in request.data and request.data['isFunction']:
                    new_data['isFunction'] = request.data['isFunction'] 
                # else:
                #     return {"error": True, "message": "please provide is_staff", "status": 400}
                if 'isActive' in request.data and request.data['isActive']:  
                    new_data['isActive'] = request.data['isActive'] 
                # else:
                #     return {"error": True, "message": "please provide is_active", "status": 400}
                if 'extras' in request.data and request.data['extras']:  
                    new_data['extras'] = request.data['extras'] 
                # else:
                #     return {"error": True, "message": "please provide is_superuser", "status": 400}
                if 'is_deleted' in request.data and request.data['is_deleted']:  
                    new_data['is_deleted'] = request.data['is_deleted'] 
                # else:
                #     return {"error": True, "message": "please provide is_superuser", "status": 400}
                if 'created_user' in request.data and request.data['created_user']:  
                    new_data['created_user'] = request.data['created_user'] 
                # else:
                #     return {"error": True, "message": "please provide is_superuser", "status": 400}
                new_data['created_at'] = datetime.datetime.now() 
                # else:
                #     return {"error": True, "message": "please provide is_superuser", "status": 400}
                if 'updated_user' in request.data and request.data['updated_user']:  
                    new_data['updated_user'] = request.data['updated_user'] 
                # else:
                #     return {"error": True, "message": "please provide is_superuser", "status": 400}
                new_data['updated_at'] = datetime.datetime.now() 
                # else:
                #     return {"error": True, "message": "please provide is_superuser", "status": 400}
                return (new_data)
            else:
                return {"error": True, "message": "please provide details", "status": 400}
        except Exception as ex:
            log.error(ex)
            return {"error": True, "message": f"Exception please provide details {ex}", "status": 400}
        

    def ruleAuditInsertDetails(self,request):
        try:
            log.info("ApiCallController api updateDetails")
            insert_data = {}
            if "rules_config_id" not in request.data or not request.data['rules_config_id']:
                return Response({"error": True, "message": "Rules Configuration name is required", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            
            insert_data["rules_config_id"] = request.data['rules_config_id']
            if "rules_group_id" in request.data and request.data['rules_group_id']:
                insert_data['rules_group_id'] = request.data['rules_group_id']
            else:
                {"error": True, "message": "Rules rules_group_id is required", "status": 400}
            if "field_name" in request.data and request.data['field_name']:
                insert_data['field_name'] = request.data['field_name']
            else:
                {"error": True, "message": "Rules field_name name is required", "status": 400}

            if "old_value" in request.data and request.data['old_value']:
                insert_data['old_value'] = request.data['old_value']
            else:
                return {"error": True, "message": "Rules old_value is required", "status": 400}

            if "new_value" in request.data and request.data['new_value']:
                insert_data['new_value'] = request.data['new_value']
            else:
                return {"error": True, "message": "Rules new_value is required", "status": 400}
            
            if "user" in request.data and request.data['user']:
                insert_data['user'] = request.data['user']
            else:
                return {"error": True, "message": "Rules user is required", "status": 400}

            if "extras" in request.data and request.data['extras']:
                insert_data['extras'] = request.data['extras']


            if "is_deleted" in request.data and request.data['is_deleted']:
                insert_data['is_deleted'] = request.data['is_deleted']
            else:
                return {"error": True, "message": "Rules is_deleted is required", "status": 400}

            if "isActive" in request.data and request.data['isActive']:
                insert_data['isActive'] = request.data['isActive']
            else:
                return {"error": True, "message": "Rules isActive is required", "status": 400}
            if "created_user" in request.data and request.data['created_user']:
                insert_data['created_user'] = request.data['created_user']
            else:
                return {"error": True, "message": "Rules created_user is required", "status": 400}
            insert_data['created_at'] = datetime.datetime.now()

            if "updated_user" in request.data and request.data['updated_user']:
                insert_data['updated_user'] = request.data['updated_user']
            else:
                return {"error": True, "message": "Rules updated_user is required", "status": 400}

            insert_data['updated_at'] = datetime.datetime.now()
            return insert_data
        except Exception as ex:
            log.info(ex)
            return Response({"error": True, "message": f"we would like to inform you {ex}", "status": 400}, status=status.HTTP_400_BAD_REQUEST)


