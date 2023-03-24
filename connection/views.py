import itertools
import json
import logging
import copy
import os
import types
import datetime

""" Import Django libraries """
from django.shortcuts import render
from django.conf import settings
from django.http import JsonResponse
from django.db.models import Q
from django.contrib.auth.models import User
from django.db.models.functions import Concat
from django.db.models import CharField, Value as V

""" Import rest framework libraries """
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import status

from connection.models import ConnectionType, FieldMaster, Connection, StatusEnum
from connection.serializers import ConnectionHistorySerializer, ConnectionTypeSerializer, ConnectionUpdateSerializer, FieldMasterSerializer, ConnectionSerializer,ConnectionListSerializer, ConnectionViewSerializer, ConnectionTypeViewSerializer,  ConnectionCreateSerializer, ListSerializer
from common.common import test_connection
from connection.controller.historyController import HistoryController

from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi

from deepdiff import DeepDiff

# Get an instance of a logging
log = logging.getLogger(__name__)

class ConnectionViewSet(ViewSet):

    @swagger_auto_schema(
        responses = {
            '200' : 'List of fields based on connection type',
            '400': 'Bad Request'
        }
    )
    def new(self, request):
        """
        Return a list of fields based on Connection type
        """
        try:
            # Application sucess content

            result = []
            model_data = ConnectionType.objects.filter(status=1).all()
            serializer = ConnectionTypeSerializer(model_data, many=True)

            for data in serializer.data:
                result_data = {}
                fields = []
                for input in data['input_field_id']:
                    field_data = FieldMaster.objects.filter(field_master_id__in=input)
                    field_master_values = FieldMasterSerializer(field_data, many=True)
                    fields.append(field_master_values.data)
                data.pop('input_field_id')
                result_data = copy.deepcopy(data)
                result_data['fields'] = fields
                result.append(result_data)

            response_data = {'connection': result}
            response_content = {"error": False, "message": "Success", "status": 200, "data": response_data}
            return Response(response_content, status=status.HTTP_200_OK)
        except Exception as e:
            # Application failure content
            return Response({"error": False, "message": e, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
              
    @swagger_auto_schema(
        request_body=ConnectionCreateSerializer,
        responses = {
            '200' : ConnectionCreateSerializer,
            '400': 'Bad Request'
        }
    )
    def create(self, request):
        """
        Create a new connection with given connection_type_id
        """
        try:
            # Application success content
            if request.data:
                new_data = {}
                parameter = {}
                connection_type_id = 0

                if "connection_type_id" in request.data:
                    connection_type_id = request.data['connection_type_id']
                else:
                    return Response({"error": False, "message": "Invalid Connection Type ID", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

                if "parameter" in request.data:
                    parameter = request.data['parameter']
                else:
                    return Response({"error": False, "message": "Invalid Parameter data", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)

                # Get connection type data
                connection_type_data = ConnectionType.objects.get(connection_type_id=connection_type_id)
                connection_count = Connection.objects.filter(connection_type_id=connection_type_id).count()
                if "connection_name" in request.data and request.data['connection_name']:
                    connection_name = Connection.objects.filter(name=request.data['connection_name'])
                    if not connection_name:
                        new_data['name'] = request.data['connection_name']
                    else:    
                        return Response({"error": False, "message": "connection name already exists ", "status": status.HTTP_400_BAD_REQUEST}, status=status.HTTP_400_BAD_REQUEST)
                else:  
                    new_data['name'] = connection_type_data.connection_type+'_'+connection_type_data.connection_type_name+'_'+str(connection_count)
                
                new_data['parameter'] = request.data['parameter']
                validated_parameter = self.validateurl(request.data['parameter'])
                if validated_parameter:
                    new_data['parameter'] = validated_parameter
                    parameter = validated_parameter
                new_data['created_by'] = request.user.id
                new_data['status'] = StatusEnum.Active.value
                new_data['connection_type_id'] = connection_type_id
                new_data['is_deleted'] = False

                connection_type = connection_type_data.connection_type
                connection_test = self.validateconnection(connection_type, parameter, '')
                required_fields = self.validateparameter(connection_type_id, parameter)

                # Save data when mandatory fields are available
                flag = False
                message = 'Connection not created'
                connection_type_excluded = ("fileupload", "supportfirst", "superset")
                if required_fields['status']:
                    if not connection_test:
                        if connection_type_data.application_code not in connection_type_excluded:
                            flag, message = test_connection(request)
                        if flag or connection_type_data.application_code in connection_type_excluded:
                            connection_data = ConnectionSerializer(data=new_data)
                            if connection_data.is_valid():
                                obj = connection_data.save()
                                # Connection History
                                historyStatus = "Create Connection"
                                connection_history = HistoryController()
                                connection_history.history_create(connection_id = obj.connection_id, user_id = 1, table_name = "connection", history_status = historyStatus, description=new_data['name'] +" Connection added", changed_attributes=new_data)

                                new_data['connection_id'] = obj.connection_id
                                response_content = {"error": False, "message": "Successfully Created",
                                                    "status": status.HTTP_200_OK, "data": new_data}
                            else:
                                response_content = {"error": False, "message": connection_data.errors,
                                                    "status": status.HTTP_400_BAD_REQUEST}
                        else:
                            response_content = {"error": False, "message": message,
                                                "status": status.HTTP_400_BAD_REQUEST}
                    else:
                        response_content = {"error": False, "message": "Connection Already exists with same details",
                                            "status": status.HTTP_400_BAD_REQUEST}
                else:
                    message = 'Please provide the following data for parameter : ' + ', '.join(
                        required_fields['data'])
                    response_content = {"error": False, "message": message, "status": status.HTTP_400_BAD_REQUEST}

                return Response(response_content, status=response_content['status'])
            else:
                return Response({"error": False, "message": "Invalid data", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Application failure content
            return Response({"error": False, "message": e, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    def validateparameter(self, connection_type_id, parameter):
        # To validate the input parameter fields are required
        model_data = ConnectionType.objects.get(connection_type_id=connection_type_id)
        serializer = ConnectionTypeSerializer(model_data)
        field_master_ids = list(itertools.chain.from_iterable(serializer.data['input_field_id']))
        field_master_data = FieldMaster.objects.exclude(field_type='header').filter(field_master_id__in=field_master_ids).values_list(
            'field_code', 'required')
        required_fields = []
        field_data = dict(field_master_data)

        for fields in field_data:
            if fields not in parameter and field_data[fields] is True:
                required_fields.append(fields)

        if len(required_fields) == 0:
            return {"status": True, "data": required_fields}
        else:
            return {"status": False, "data": required_fields}

    def validateconnection(self, connection_type, parameter, connection_id):
        connection_data = {}
        if connection_type != "Manual" and not connection_id:
            connection_data = Connection.objects.filter(parameter=parameter, is_deleted=False)
        elif connection_type != "Manual" and connection_id:
            connection_data = Connection.objects.exclude(connection_id=connection_id).filter(parameter=parameter, is_deleted=False).values_list('connection_id')
        return connection_data

    def validateurl(self, parameter):
        parameter_data = json.loads(parameter,strict=False)
        if 'url' in parameter_data and not parameter_data['url'].endswith('/'):
            parameter_data['url'] = parameter_data['url'] + "/"
        parameter = json.dumps(parameter_data)
        return parameter

    @swagger_auto_schema(
        responses = {
            '200' : 'List of connections',
            '400': 'Bad Request'
        }
    )
    def list(self, request):
        """Return all connection, ordered by recently created
        """
        try:
            # Application success content
            response_content = {"error":False, "message":"success", "data": "", "status":200}
            condition = Q(is_deleted= False)
            # log.info("User Email - {}".format(request.user.email))
            # group_members = AuthView.get_user_specific_roles(self, request.user.email, client_id = "opexwiseapi")
            # log.info("Group members - {}".format(group_members))
            # if isinstance(group_members, list) and "all" not in group_members:
            #     condition &= Q(created_by__in = group_members)
            # elif not group_members:
            #     condition &= Q(created_by = request.user.id)
            query_set = Connection.objects.filter(condition).all()
            serializer = ConnectionListSerializer(query_set, many= True)

            if serializer.data:
                response_content['data'] = {
                    'connection':serializer.data
                }
            else:
                response_content['page_access'] = False

            return Response(response_content, status= status.HTTP_200_OK)
        except Exception as e:
            # Application failure content
            return Response({"error": False, "message": e, "status": 400}, status= status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        request_body=ConnectionUpdateSerializer,
        responses = {
            '200' : ConnectionUpdateSerializer,
            '400': 'Bad Request'
        }
    )
    def update(self,request,connection_id,*args,**kwargs):
        '''
        Updates the Connection item with given connection_id if exists
        '''
        response_content = {"error": True, "message": "", "status": status.HTTP_400_BAD_REQUEST}
        try:
            if connection_id:
                # Application success content
                try:
                    old_value = {}
                    connection_data = Connection.objects.get(pk = connection_id, is_deleted=False)
                    connection_serializer = ConnectionSerializer(connection_data)
                    old_value = connection_serializer.data
                    
                    data = request.data
                    connection_data.status = data.get('status',connection_data.status)
                    if connection_data and 'status' in request.data and request.data['status'] in ("2", 2):
                        condition = Q(source_connection_id=connection_id, is_deleted=False)
                        condition.add(Q(destination_connection_id=connection_id, is_deleted=False), Q.OR)                                   
                        datamap_data = DataMap.objects.filter(condition)
                        if datamap_data:
                            return Response({"error": True, "message": "Warning: Connection currently in use. Cannot change state", "status": status.HTTP_403_FORBIDDEN}, status=status.HTTP_403_FORBIDDEN)                         

                    connection_type_id = request.data['connection_type_id']
                    parameter = request.data['parameter']
                    validated_parameter = self.validateurl(request.data['parameter'])
                    if validated_parameter:
                        parameter = validated_parameter
                    connection_type_data = ConnectionType.objects.get(connection_type_id=connection_type_id)
                    connection_type = connection_type_data.connection_type
                    connection_test = self.validateconnection(connection_type, parameter, connection_id)
                    validated = self.validateparameter(connection_type_id, parameter)

                    flag = False
                    message = ''
                    connection_type_excluded = ("fileupload", "supportfirst", "superset")
                    if validated['status']:
                        if not connection_test:
                            if connection_type_data.application_code not in connection_type_excluded:
                                flag, message = test_connection(request)
                            if flag or connection_type_data.application_code in connection_type_excluded:
                                connection_data.name = data.get('name',connection_data.name)
                                connection_data.description = data.get('description',connection_data.description)
                                if parameter:
                                    connection_data.parameter = parameter
                                else:
                                    connection_data.parameter = data.get('parameter',connection_data.parameter)
                                connection_data.updated_by = request.user.id
                                connection_data.updated_date = datetime.datetime.now()
                                connection_data.save()

                                serializer = ConnectionSerializer(connection_data)

                                if old_value:
                                    connection_history = HistoryController()
                                    values_changed = DeepDiff(old_value,serializer.data, exclude_paths = ["root['connection_id']", "root['is_deleted']", "root['created_by']", "root['created_date']", "root['updated_by']", "root['updated_date']"], ignore_order = True, report_repetition=True, ignore_type_in_groups=[(str, bytes, datetime.datetime)])
                                    connection_history.history_data_format(values_changed, connection_data, 1, "connection", connection_id, name = connection_data.name + " connection")
                                
                                response_content['message'] = 'Connection Id: '+str(connection_id)+' updated successfully'
                                response_content['status']= status.HTTP_200_OK
                                response_content['error']= False
                                response_content['data']= serializer.data
                            else:
                                response_content['message'] = message
                        else:
                            response_content = {"error": False, "message": "Connection Already exists with same details",
                                                "status": status.HTTP_400_BAD_REQUEST}
                    else:
                        response_content['message']= 'Invalid parameter data'
                except Connection.DoesNotExist:
                    response_content['message']= 'No record found'
            else:
                response_content['message']= 'Invalid connection id'
        except Exception as e:
            # Application failure content
            response_content['message']= e

        return Response(response_content, status=response_content['status'])

    @swagger_auto_schema(
        responses = {
            '200' : 'Deletes the connection with given connection_id if exists',
            '400': 'Bad Request'
        }
    )
    def delete(self, request, connection_id ,*args, **kwargs):
        """
        Deletes the Connection item with given connection_id if exists
        """
        response_content = {"error": True, "message": "", "status": status.HTTP_400_BAD_REQUEST}

        try:
            if connection_id:
                # Application success content
                try:
                    #connection = Connection.objects.get(pk = connection_id, is_deleted=False, status=StatusEnum.Active.value)
                    connection = Connection.objects.get(pk=connection_id, is_deleted=False)
                    if connection:
                        source_datamap = ''
                        destination_datamap = ''
                        # source_datamap = DataMap.objects.filter(source_connection_id=connection_id, is_deleted=False)
                        # destination_datamap = DataMap.objects.filter(destination_connection_id=connection_id, is_deleted=False)
                        if source_datamap or destination_datamap:
                            response_content['message'] = "Cannot delete Connection if it is active in Data mapping"
                        else:
                            connection.is_deleted = True
                            connection.status= StatusEnum.Inactive.value
                            connection.updated_by = request.user.id
                            connection.updated_date = datetime.datetime.now()
                            connection.save()

                            # Connection Delete History
                            historyStatus = "Delete Connection"
                            connection_history = HistoryController()
                            connection_history.history_create(connection_id = connection_id, user_id = 1, table_name = "connection", history_status = historyStatus, description=connection.name +" Connection deleted", changed_attributes=connection)

                            response_content['message'] = 'Connection Id: '+str(connection_id)+' deleted successfully'
                            response_content['error'] = False
                            response_content['status'] = status.HTTP_200_OK

                    else:
                        response_content['message'] = 'No record found'
                except Connection.DoesNotExist:
                    response_content['message'] = 'No record found'
            else:
                response_content['message'] = 'Invalid connection id'
        except Exception as e:
            # Application failure content
            response_content['message'] = e

        return Response(response_content,status=response_content['status'])


    connection_id = openapi.Parameter('connection_id', in_=openapi.IN_QUERY, type=openapi.TYPE_STRING)
    @swagger_auto_schema(
        manual_parameters=[connection_id],
        responses = {
            '200' : 'Returns Connection based on the connection id',
            '400': 'Bad Request'
        }
    )
    def view(self, request, connection_id ,*args, **kwargs):
        """
        Return a connection item with given connection_id if exists 
        """
        response_content = {"error": True, "message": "", "status": status.HTTP_400_BAD_REQUEST}
        try:
            # Application sucess content
            if connection_id:
                try:
                    connection_data = Connection.objects.get(connection_id= connection_id, is_deleted=False)
                    serializer = ConnectionViewSerializer(connection_data)

                    fields = []
                    for input in connection_data.connection_type_id.input_field_id:
                        field_data = FieldMaster.objects.filter(field_master_id__in=input)
                        field_master_values = FieldMasterSerializer(field_data, many=True)
                        fields.append(field_master_values.data)

                    connection_type_data = ConnectionType.objects.get(connection_type_id=connection_data.connection_type_id.connection_type_id)
                    connection_type_serializer = ConnectionTypeViewSerializer(connection_type_data)
                    data = connection_type_serializer.data
                    data['fields']= fields

                    response_data= {"connection":[], "data":{}}
                    response_data["data"]= serializer.data
                    response_data["connection"].append(data)

                    response_content["message"]= 'success'
                    response_content["status"]= status.HTTP_200_OK
                    response_content["error"]= False
                    response_content["data"]= response_data

                except Connection.DoesNotExist:
                    response_content['message']= 'No record found'
            else:
                response_content['message']= 'Invalid connection id'
        except Exception as e:
            # Application failure content
            response_content['message']= e

        return Response(response_content, status=response_content['status'])

    @swagger_auto_schema(
        request_body=ConnectionCreateSerializer,
        responses = {
            '200' : ConnectionCreateSerializer,
            '400': 'Bad Request'
        }
    )
    def test_connection(self, request):
        """
        Return a http response after testing the connection details
        """
        try:
            log.info("Testing connection")
            flag, message = test_connection(request)
            if flag:
                return Response({"error": False, "message": message, "status": 200}, status=status.HTTP_200_OK)
            else:
                return Response({"error": True, "message": message, "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            log.error(e)
            return Response({"error": True, "message": e, "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses = {
            '200' : 'Datamap list for the given connection id',
            '400': 'Bad Request'
        }
    )
    def datamap_view(self, request, connection_id ,*args, **kwargs):
        """
        Returns a datamap with the given connection_id if exists
        """
        response_content = {"error": True, "message": "", "status": status.HTTP_400_BAD_REQUEST}
        try:
            # Application sucess content
            if connection_id:
                try:
                    result = []
                    connection_data = Connection.objects.get(connection_id= connection_id, is_deleted=False)
                    if connection_data:
                        condition = Q(source_connection_id=connection_id, is_deleted=False)
                        condition.add(Q(destination_connection_id=connection_id, is_deleted=False), Q.OR)                                   
                        datamap_data = DataMap.objects.filter(condition)
                        if datamap_data:  
                            datamap_response = DataMapSerializer(datamap_data, many= True)
                            result = datamap_response.data

                    response_content["message"]= 'success'
                    response_content["status"]= status.HTTP_200_OK
                    response_content["error"]= False
                    response_content["data"]= result
                except Connection.DoesNotExist:
                    response_content['message']= 'No record found'
            else:
                response_content['message']= 'Invalid connection id'
        except Exception as e:
            log.error(e)
            response_content['message']= e

        return Response(response_content, status=response_content['status'])

    @swagger_auto_schema(
        request_body=ListSerializer,
        responses = {
            '200' : 'Connection list',
            '400': 'Bad Request'
        }
    )
    def connection_list(self, request):
        """
        Return all connection with limit and offset, ordered by recently created
        """
        try:
            # Application success content
            response_content = {"error":False, "message":"success", "data": "", "status":200}
            condition = Q(is_deleted= False)
            # log.info("User Email - {}".format(request.user.email))
            # group_members = AuthView.get_user_specific_roles(self, request.user.email, client_id = "opexwiseapi")
            # log.info("Group members - {}".format(group_members))
            # if isinstance(group_members, list) and "all" not in group_members:
            #     condition &= Q(created_by__in = group_members)
            # elif not group_members:
            #     condition &= Q(created_by = request.user.id)
            if "search_content" in request.data and request.data['search_content'] :
                or_condition = Q(name__icontains = request.data['search_content'])
                or_condition.add(Q(connection_id__icontains = request.data['search_content']), Q.OR)
                or_condition.add(Q(connection_type_id__in = ConnectionType.objects.filter(connection_type_name__icontains = request.data['search_content']).values_list('connection_type_id', flat=True)), Q.OR)
                or_condition.add(Q(connection_type_id__in = ConnectionType.objects.filter(connection_type_description__icontains = request.data['search_content']).values_list('connection_type_id', flat=True)), Q.OR)
                status_list = {"Active" : "1", "Inactive" : "2", "Draft" : "3", "New" : "4", "Running" : "5", "Pause" : "6", "Stopped" : "7", "Failed" : "8"}
                status_key=list(value for value in status_list if request.data['search_content'] in value.lower())
                if status_key:
                    for se_value in status_key:
                        if se_value in status_list:
                            w_status = status_list[se_value]
                            or_condition.add(Q(status__icontains = w_status), Q.OR)
                or_condition.add(Q(created_by__in = User.objects.annotate(fullname=Concat('first_name', V(' ') ,'last_name')).filter(fullname__icontains = request.data['search_content']).values_list('id', flat=True)), Q.OR)
                or_condition.add(Q(updated_by__in = User.objects.annotate(fullname=Concat('first_name', V(' ') ,'last_name')).filter(fullname__icontains = request.data['search_content']).values_list('id', flat=True)), Q.OR)
                condition &= or_condition

            total_count = 0
            limit = settings.LIMIT
            offset = settings.OFFSET
            if 'offset' in request.data and request.data['offset']:
                offset = request.data['offset']
            if 'limit' in request.data and request.data['limit']:
                limit = request.data['limit']
            total_count = Connection.objects.filter(condition).count()
            query_set = Connection.objects.filter(condition).order_by('-connection_id').all()[int(offset):int(offset) + int(limit)]
            serializer = ConnectionListSerializer(query_set, many= True)
            if serializer.data:
                response_content["count"] = total_count
                response_content['data'] = {
                    'connection':serializer.data
                }
            else:
                response_content['page_access'] = False
                
            return Response(response_content, status= status.HTTP_200_OK)
        except Exception as e:
            # Application failure content
            return Response({"error": False, "message": e, "status": 400}, status= status.HTTP_400_BAD_REQUEST)


class ConnectionHistoryView(ViewSet):

    @swagger_auto_schema(
        request_body=ConnectionHistorySerializer,
        responses = {
            '200' : 'Connection History list',
            '400': 'Bad Request'
        }
    )
    def list(self, request):
        """
        Returns the history a Connection with the given connection_id of exists
        """
        try:
            # Application sucess content
            log.info(request.data)
            if "connection_id" not in request.data or not request.data['connection_id']:
                return Response({"error": True, "message": "Input connection id missing ", "status": 400},
                                status=status.HTTP_400_BAD_REQUEST)

            response_content = {"error": False, "message": "Success", "status": 200, "count": 0, "data": ""}
            
            if "field_value" in request.data:
                connection_history = HistoryController()
                ch_serializer_data = connection_history.grouping(request.data['connection_id'],request.data['field_value'])
            else:
                connection_history = HistoryController()
                ch_serializer_data = connection_history.grouping(request.data['connection_id'])
            
            response_content['count'] = ch_serializer_data['count']
            response_content['data'] = ch_serializer_data['data']
            return Response(response_content, status=status.HTTP_200_OK)
        except Exception as e:
            # Application failure content
            return Response({"error": True, "message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

class NlpAnalysisView(ViewSet):
    permission_classes = []
    
    def nlp_analysis(self, request):
        """
        Return a http response
        """
        try:
            # Application sucess content
            if request.method == 'GET':
                return Response({"error": False, "message":"Success", "status": 200 }, status=status.HTTP_200_OK)
            elif request.method == 'POST':
                if request.data:
                    log.info(request.data)
                    if not os.path.isdir(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, settings.NLPANALYSIS_STATUS)):
                        os.mkdir(os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, settings.NLPANALYSIS_STATUS))

                    folder_path = os.path.join(settings.MEDIA_ROOT, settings.NLPANALYSIS_STATUS)
                    now=datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S')
                    file_name =  str("nlpanalysis_status_"+now)+'.txt'
                    file_path = folder_path+file_name
                    f = open( file_path, 'w+')
                    data = json.dumps(request.data)
                    f.write(data)
                    f.close()
                    return Response({"error": False, "message":"Success", "data": data, "status": 200 }, status=status.HTTP_200_OK)
                else:
                    return Response({"error": False, "message":"No data found", "status": 200 }, status=status.HTTP_200_OK)   

        except Exception as e:
            # Application failure content
            log.error(e)
            return Response({"error": True, "message": str(e), "status": 400}, status=status.HTTP_400_BAD_REQUEST)

