from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from django.db.models import Q
from django.conf import settings
from rule_engine.models import TBLRules, CommonMaster, TBLRulesSet
from rule_engine.serializers import TBLRulesSerializer, CommonMasterSerializer
import logging
import datetime

log = logging.getLogger(__name__)
pattern = "\W"

class CommonMasterView(ViewSet):
    def list(self, request):
        try:
            response_content = {"error": False, "message": "Success", "status": 200, "count": 0, "data": ""}
            condition = Q(is_deleted= False)
            if "query_type" not in request.data or not request.data['query_type']:
                return Response({"error": True, "message": "Query Type is required", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            if request.data['query_type']:
                condition &= Q(cm_type = request.data['query_type'])
            query_set = CommonMaster.objects.filter(condition).order_by('cm_order')
            serializer = CommonMasterSerializer(query_set, many=True)
            if serializer.data :
                result = serializer.data
            response_content["data"] = result    
            return Response(response_content, status=status.HTTP_200_OK)

        except Exception as e:
            # Application failure content
            log.error(e)
            print(e)
            return Response({"error": True, "message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)
    
class RuleEngineView(ViewSet):

    def list(self, request):
        try:
            log.info(request.data)
            response_content = {"error": False, "message": "Success", "status": 200, "count": 0, "data": ""}
            condition = Q(is_deleted= False)
            total_count = 0
            result = []
            limit = settings.LIMIT
            offset = settings.OFFSET
            if 'offset' in request.data and request.data['offset']:
                offset = request.data['offset']
            if 'limit' in request.data and request.data['limit']:
                limit = request.data['limit']
            # search_content    
            if "search_content" in request.data and request.data['search_content'] :
                or_condition = Q(rules_name__icontains = request.data['search_content'])
                # or_condition.add(Q(destination_connection_id__in = Connection.objects.filter(name__icontains = request.data['search_content']).values_list('connection_id', flat=True)), Q.OR)
                condition &= or_condition
            active_count = TBLRules.objects.filter(condition, isActive=True).count()
            total_count = TBLRules.objects.filter(condition).count()
            query_set = TBLRules.objects.filter(condition).order_by('-rules_id')[int(offset):int(offset) + int(limit)]
            serializer = TBLRulesSerializer(query_set, many=True)
            if serializer.data :    
                for t_set in serializer.data:
                    if t_set['isActive']:
                        isActive = CommonMaster.objects.filter(cm_type = 'rules_status', cm_value=1).values('cm_name')
                        if isActive:
                            t_set['status_name'] = isActive[0]['cm_name']
                    else :    
                        isActive = CommonMaster.objects.filter(cm_type = 'rules_status', cm_value=2).values('cm_name')
                        if isActive:
                            t_set['status_name'] = isActive[0]['cm_name']
                    if t_set['isOpty']:
                        isOpty = CommonMaster.objects.filter(cm_type = 'rules_type', cm_value=1).values('cm_name')
                        if isOpty:
                            t_set['rule_type'] = isOpty[0]['cm_name']
                    else :    
                        isOpty = CommonMaster.objects.filter(cm_type = 'rules_type', cm_value=2).values('cm_name')
                        if isOpty:
                            t_set['rule_type'] = isOpty[0]['cm_name']
                    t_set['rule_set_count'] = TBLRulesSet.objects.filter(rules_id = t_set['rules_id'], is_deleted= False).count()
                    result.append(t_set)
            response_content["count"] = total_count 
            response_content["active_count"] = active_count 
            response_content["data"] = result            
            return Response(response_content, status=status.HTTP_200_OK)

        except Exception as e:
            # Application failure content
            log.error(e)
            print(e)
            return Response({"error": True, "message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)
 
    def create(self, request):
        """Return a http response

        Optional plotz says to frobnicate the bizbaz first.
        """
        try:
            log.info(request.data)
            insert_data = {}
            if "rules_name" not in request.data or not request.data['rules_name']:
                return Response({"error": True, "message": "Rules name is required", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            
            if "rules_name" in request.data and request.data['rules_name']:
                model_name = TBLRules.objects.filter(rules_name=request.data['rules_name'].strip())
                if model_name:  
                    return Response( {"error": True, "message": "Rules name already exists ", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            insert_data['rules_name'] = request.data['rules_name'].strip()
            insert_data['rules_sequence'] = request.data['rules_sequence']
            if "rule_type" in request.data and request.data['rule_type']:
                if request.data['rule_type'] == '1':
                    insert_data['isOpty'] = True
                else:    
                    insert_data['isOpty'] = False
            else:    
                insert_data['isOpty'] = True

            if "extra" in request.data and request.data['extra']:
                insert_data['extra'] = request.data['extra']  
            if "status" in request.data and request.data['status']:
                if request.data['status'] == '1':
                    insert_data['isActive'] = True
                else:    
                    insert_data['isActive'] = False
            else:    
                insert_data['isActive'] = True
            # insert_data['created_by'] = request.user.id
            insert_data['created_user'] = 1
            insert_data['updated_user'] = 1
            insert_data['updated_at']=datetime.datetime.now()
            print(insert_data)
            data_save = TBLRulesSerializer(data = insert_data)  
            if data_save.is_valid():
                tm_inserted_id=data_save.save()  
                data = { "rules_id" : tm_inserted_id.rules_id }   
                return Response( {"error": False, "message": "success", "data" : data } , status=status.HTTP_200_OK)
            else:
                return Response({"error": True, "message": str(data_save.errors), "status": 400}, status=status.HTTP_400_BAD_REQUEST)   

        except Exception as e:
            # Application failure content
            log.error(e)
            print(e)
            return Response({"error": True, "message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as err:
            log.error(err)
            return Response({"error": True, "message": str(err), "status": 400}, status=status.HTTP_400_BAD_REQUEST)
   
    def update(self, request):
        """Return a http response

        Optional plotz says to frobnicate the bizbaz first.
        """
        try:
            log.info(request.data)
            if "rules_id" not in request.data or not request.data['rules_id']:
                return Response({"error": True, "message": "Rules Id is required", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
           
            if "rules_name" not in request.data or not request.data['rules_name']:
                return Response({"error": True, "message": "Rules name is required", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            
            if "rules_name" in request.data and request.data['rules_name']:
                model_name = TBLRules.objects.filter(rules_name=request.data['rules_name'].strip(), is_deleted=False).exclude(rules_id = request.data['rules_id'])
                if model_name:  
                    return Response( {"error": True, "message": "Rules name already exists ", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            get_data = TBLRules.objects.get(pk = request.data['rules_id'], is_deleted=False)
            if get_data:    
                if request.data['rules_name'].strip():
                    get_data.rules_name = request.data['rules_name'].strip()
                if request.data['rules_sequence']:    
                    get_data.rules_sequence = request.data['rules_sequence']
                if "rule_type" in request.data and request.data['rule_type']:
                    if request.data['rule_type'] == '1':
                        get_data.isOpty = True
                    else:    
                        get_data.isOpty = False
                if "extra" in request.data and request.data['extra']:
                    get_data.extra = request.data['extra']  
                if "status" in request.data and request.data['status']:
                    if request.data['status'] == '1':
                        get_data.isActive = True
                    else:    
                        get_data.isActive = False                
                get_data.updated_user = 1
                get_data.updated_at=datetime.datetime.now()
                get_data.save()
                data = { "rules_id" : request.data['rules_id'] }   
                return Response( {"error": False, "message": "success", "data" : data } , status=status.HTTP_200_OK)
                # else:
                #     return Response({"error": True, "message": str(data_save.errors), "status": 400}, status=status.HTTP_400_BAD_REQUEST)   
            else:
                return Response({"error": True, "message": "Record Not found", "status": 400}, status=status.HTTP_400_BAD_REQUEST)   
        except TBLRules.DoesNotExist:
            return Response({"error": True, "message": 'No record found', "status": 400}, status=status.HTTP_400_BAD_REQUEST)      
        except Exception as e:
            # Application failure content
            log.error(e)
            print(e)
            return Response({"error": True, "message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        except KeyError as err:
            log.error(err)
            return Response({"error": True, "message": str(err), "status": 400}, status=status.HTTP_400_BAD_REQUEST)
   
    def view(self, request):
        try:
            log.info(request.data)
            response_content = {"error": False, "message": "Success", "status": 200, "count": 0, "data": ""}

            if "rules_id" not in request.data or not request.data['rules_id']:
                return Response({"error": True, "message": "Rules Id is required", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            get_data = TBLRules.objects.get(pk = request.data['rules_id'], is_deleted=False)
            if get_data:
                result = []           
                query_set = TBLRules.objects.filter(rules_id = request.data['rules_id'], is_deleted=False)
                print(query_set)
                serializer = TBLRulesSerializer(query_set, many=True)
                if serializer.data :    
                    for t_set in serializer.data:
                        if t_set['isActive']:
                            t_set['status_name'] = 1
                        else :    
                            t_set['status_name'] = 2
                        if t_set['isOpty']:
                            t_set['rule_type'] = 1
                        else :    
                            t_set['rule_type'] = 2
                        t_set['rule_set_count'] = 1
                        result = t_set
                response_content["data"] = result            
                return Response(response_content, status=status.HTTP_200_OK)
        
        except TBLRules.DoesNotExist:
            return Response({"error": True, "message": 'No record found', "status": 400}, status=status.HTTP_400_BAD_REQUEST)      
        except Exception as e:
            # Application failure content
            log.error(e)
            print(e)
            return Response({"error": True, "message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)
    

    def delete(self, request):
        """
        Deletes the Rules item with given rules if exists
        """
        response_content = {"error": True, "message": "", "status": status.HTTP_400_BAD_REQUEST}
        try:
            if request.data['rules_id']:
                # Application success content
                try:
                    rules_query = TBLRules.objects.get(pk=request.data['rules_id'], is_deleted=False)
                    if rules_query:                       
                        rules_query.is_deleted = True
                        # rules_query.updated_user = request.user.id
                        rules_query.updated_user = 1
                        rules_query.updated_at = datetime.datetime.now()
                        rules_query.save()

                        response_content['message'] = 'Rules Id: '+str(request.data['rules_id'])+' deleted successfully'
                        response_content['error'] = False
                        response_content['status'] = status.HTTP_200_OK
                    else:
                        response_content['message'] = 'No record found'
                except TBLRules.DoesNotExist:
                    response_content['message'] = 'No record found'
                except ValueError as e:
                    response_content['message'] = 'Invalid Rules id'
            else:
                response_content['message'] = 'Invalid Rules id'
        except Exception as e:
            # Application failure content
            response_content['message'] = e

        return Response(response_content,status=response_content['status'])

