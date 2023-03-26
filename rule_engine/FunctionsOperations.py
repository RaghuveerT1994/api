from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from django.db.models import Q
from django.conf import settings
from rule_engine.models import TBLRuleFunctionsOperation
from rule_engine.serializers import TBLRulesFunctionOperationSerializer
from rule_engine.controller.RuleFunctionalOperationsController import RuleFunctionalOperationsController
import logging
import datetime

log = logging.getLogger(__name__)
pattern = "\W"

class RuleEngineFunctionalOperationView(ViewSet):

    def create(self,request):
        try:
            log.info("ApiCallController api create record")
            if request.method == "POST":  
                if request.data:
                    try:
                        existing_record = TBLRuleFunctionsOperation.objects.get(functions_name=request.data['functions_name'])
                        return Response({"error": True, "message": 'record already exist', "status": 400}, status=status.HTTP_400_BAD_REQUEST)      
                    except TBLRuleFunctionsOperation.DoesNotExist:
                        if request.data['created_user'] and "created_user" in request.data:
                            record = TBLRuleFunctionsOperation.objects.create(functions_name=request.data["functions_name"],isOpertion=request.data["isOperation"]
                                                                          ,isFuntion=request.data["isFunction"],is_deleted=request.data["is_deleted"],
                                                                          isActive=request.data["isActive"],extras = request.data["extras"],created_user=request.data["created_user"],
                                                                          created_at=request.data["created_at"],updated_user=request.data["updated_user"],updated_at=request.data["updated_at"])
                            return Response({"error": False, "message": " record created", "status": 200}, status=status.HTTP_200_OK)
                        else:
                            return Response({"error": True, "message": 'record found already exist', "status": 400}, status=status.HTTP_400_BAD_REQUEST)      

                        # updated_data = userController.UserController.updateUserDetails(self,request,self)
                        # user_data = userSerializer(existing_record,data=updated_data,partial=True)
                else:
                    return Response({"error": False, "message": "data missing", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error": True, "message": f"we would like to inform you {ex}", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        


    def update(self,request):
        try:
            print("inside try1")
            log.info("ApiCallController api update record")
            if request.method == "POST":  
                if request.data:
                    try:
                        print("inside try")
                        existing_record = TBLRuleFunctionsOperation.objects.get(functions_id=request.data['functions_id'])
                        print(existing_record)
                        updated_data = RuleFunctionalOperationsController.ruleFunctionalOperationsDetails(self,request)
                        user_data = TBLRulesFunctionOperationSerializer(existing_record,data=updated_data,partial=True)
                        if user_data.is_valid():
                            obj = user_data.save()
                            return Response({"error": False, "message": "record updated successfully", "status": 200}, status=status.HTTP_200_OK)
                        else:
                            return Response({"error": True, "message": 'failed to update record ', "status": 400}, status=status.HTTP_400_BAD_REQUEST)
                    except TBLRuleFunctionsOperation.DoesNotExist:
                        return Response({"error": True, "message": 'failed to update record', "status": 400}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error": True, "message": 'failed to update record', "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                    return Response({"error": True, "message": 'failed to update record "POST" ', "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        except Exception  as ex:
            log.error(ex)
            return Response({"error": True, "message": f"we would like to inform you {ex} is not define", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        

    def delete(self,request):
            try:
                log.info("ApiCallController api delete record")
                if id:
                    try:
                        delete_user = TBLRuleFunctionsOperation.objects.get(functions_id=request.data["functions_id"],is_deleted=False)
                        if delete_user:
                            not_active = {
                                "is_deleted":"True"
                            }
                            datas = TBLRulesFunctionOperationSerializer(delete_user,data=not_active,partial=True)
                            if datas.is_valid():
                                obj = datas.save()
                                return Response({"error": False, "message": "record deleted successfully", "status": 200}, status=status.HTTP_200_OK)
                        else:
                            return Response({"error":True , "Message" : "data not found" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
                    except TBLRuleFunctionsOperation.DoesNotExist:
                        return Response({"error":True , "Message" : "record not found" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
                    # existing_record = User.objects.filter(id=request.data["id"]).update(is_active=False)
                else:
                    return Response({"error": False, "message": "failed", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                log.error(ex)
                return Response({"error": False, "message": f"we would like to inform you {ex}", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
            
    def list(self,request):
        try:
            log.info("ApiCallController api list")
            if not request.data:
                user_data = TBLRuleFunctionsOperation.objects.filter(is_deleted=False)
                show_data = TBLRulesFunctionOperationSerializer(user_data,many=True)
                return Response({"error": False, "message": "success", "status": 200,"Data":show_data.data}, status=status.HTTP_200_OK)
            else:
                return Response({"error":True , "Message" : "something went wrong" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error": False, "message": f"we would like to inform you {ex}", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        
    def view(self,request):
        try:
            log.info("ApiCallController api view")
            if request.data["functions_id"]:
                user_data = TBLRuleFunctionsOperation.objects.filter(pk=request.data['functions_id'],is_deleted=False) 
                if user_data:
                    show_data = TBLRulesFunctionOperationSerializer(user_data,many=True) 
                    return Response({"error": False, "message": "success", "status": 200,"Data":show_data.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"error":True , "Message" : "please put valid user id" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":True , "Message" : "functions id should not null " , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error": False, "message": f"we would like to inform you {ex}", "status": 400}, status=status.HTTP_400_BAD_REQUEST)

    def viewby(self,request):
        try:
            log.info("ApiCallController api viewby")
            if request.data["isOperation"] and request.data["isFunction"]:
                if request.data["isOperation"] != request.data["isFunction"]:
                    try:
                        user_data = TBLRuleFunctionsOperation.objects.filter(isOpertion=request.data['isOperation'],is_deleted=False,isActive=True)
                        show_data = TBLRulesFunctionOperationSerializer(user_data,many=True) 
                        return Response({"error": False, "message": "success", "status": 200,"Data":show_data.data}, status=status.HTTP_200_OK)
                    except:  
                        try:
                            user_data = TBLRuleFunctionsOperation.objects.filter(isFuntion=request.data['isFunction'],is_deleted=False,isActive=True)
                            show_data = TBLRulesFunctionOperationSerializer(user_data,many=True) 
                            return Response({"error": False, "message": "success", "status": 200,"Data":show_data.data}, status=status.HTTP_200_OK)
                        except Exception as ex:
                            log.error(ex)
                            return Response({"error": False, "message": f"we would like to inform you {ex}", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error":True , "Message" : "function and operation condition can't be same at the same time" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":True , "Message" : "Please provide condition function and operation " , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error": False, "message": f"we would like to inform you {ex}", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
