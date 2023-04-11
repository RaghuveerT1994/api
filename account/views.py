from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from django.db.models import Q
from django.conf import settings
from account.serializers import userSerializer,userShowSerializer,userDeleteSerializer,UserChangePasswordSerializer
import re
from django.contrib.auth.models import User
from django.contrib.auth.hashers import make_password
from django.contrib.auth import *
from account.controller import userController



import logging
import datetime

log = logging.getLogger(__name__)
pattern = "\W"



class UserOperationView(ViewSet):

    mail_regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,7}\b'
    pass_reg = "^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*#?&])[A-Za-z\d@$!#%*?&]{6,20}$"


    def create(self,request):
        '''create new user '''
        try:
            log.info("ApiCallController api create user")
            if request.method == "POST":     
                if request.data["password"]==request.data["confirmpassword"] and len(request.data["password"]) != 0:
                    valid = re.compile(self.pass_reg)
                    if re.fullmatch(self.mail_regex, request.data['email']) and re.search(valid,request.data['password']) :
                        try:
                            User.objects.get(username=request.data['username'])
                            return Response({"error": False, "message": 'failed (username already exist)', "status": 200}, status=status.HTTP_200_OK)
                        except User.DoesNotExist:
                            try:
                                User.objects.get(email=request.data['email'])
                                return Response({"error": False, "message": 'failed (email already exist)', "status": 200}, status=status.HTTP_200_OK)
                            except User.DoesNotExist:
                                user = User.objects.create_user(username=request.data['username'],password = make_password(request.data['password']),
                                                                email=request.data['email'],first_name=request.data['first_name'],
                                                                last_name=request.data['last_name'],is_staff=request.data['staff_status'],
                                                                is_active=request.data['active'],is_superuser=request.data['superuser'])
                                login(request,user)
                                return Response({"error": False, "message": 'User Added Successfully', "status": 200}, status=status.HTTP_200_OK) 
                    else:
                        return Response({"error": True, "message": 'failed to add user valid email and password required', "status": 400}, status=status.HTTP_400_BAD_REQUEST)

                else:
                    return Response({"error": True, "message": 'failed to add user valid password required', "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        except Exception  as ex:
            log.error(ex)
            return Response({"error": True, "message": f"we would like to inform you {ex}", "status": 400}, status=status.HTTP_400_BAD_REQUEST)

   
    def update(self,request):
        try:
            log.info("ApiCallController api update user")
            if request.method == "POST":
                if "id" in request.data and request.data['id']:
                    try:
                        existing_record = User.objects.get(pk=request.data['id'])
                        updated_data = userController.UserController.updateUserDetails(self,request,self)
                        user_data = userSerializer(existing_record,data=updated_data,partial=True)
                        if user_data.is_valid():
                            obj = user_data.save()
                        if 'error' not in updated_data:
                            return Response({"error": False, "message": "user record updated", "status": 200}, status=status.HTTP_200_OK)
                        else:
                            return Response({"error": False, "message": updated_data["message"], "status": 400}, status=status.HTTP_400_BAD_REQUEST)
                    except User.DoesNotExist:
                        return Response({"error": False, "message": 'failed to update user', "status": 200}, status=status.HTTP_200_OK)  
                else:
                    return Response({"error": False, "message": ' userid required', "status": 200}, status=status.HTTP_200_OK)  
            else:
                return Response({"error": True, "message": 'failed to update user "POST" ', "status": 400}, status=status.HTTP_400_BAD_REQUEST)

        except Exception  as ex:
            log.error(ex)
            return Response({"error": True, "message": f"we would like to inform you {ex} is not define", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        


    def delete(self,request):
        try:
            log.info("ApiCallController api delete user")
            if request.data:
                try:
                    delete_user = User.objects.get(pk=request.data['userId'],is_deleted=False)
                    if delete_user:
                        not_active = {
                            "is_active":"False",
                            "is_deleted": "True"
                        }
                        datas = userDeleteSerializer(delete_user,data=not_active)
                        if datas.is_valid():
                            obj = datas.save()
                            return Response({"error": False, "message": "user Deleted successfully", "status": 200}, status=status.HTTP_200_OK)
                    else:
                        return Response({"error":True , "message" : "data not found" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
                except User.DoesNotExist:
                    return Response({"error":True , "message" : "record not found" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
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
                user_data = User.objects.filter(is_active=True)
                show_data = userShowSerializer(user_data,many=True)
                return Response({"error": False, "message": "success", "status": 200,"data":show_data.data}, status=status.HTTP_200_OK)
            else:
                return Response({"error":True , "message" : "something went wrong" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error": False, "message": f"we would like to inform you {ex}", "status": 400}, status=status.HTTP_400_BAD_REQUEST)
        
    def view(self,request):
        try:
            log.info("ApiCallController api view")
            if request.data["id"]:
                user_data = User.objects.filter(pk=request.data['id'],is_active=True) 
                if user_data:
                    show_data = userShowSerializer(user_data,many=True) 
                    return Response({"error": False, "message": "success", "status": 200,"data":show_data.data}, status=status.HTTP_200_OK)
                else:
                    return Response({"error":True , "message" : "please put valid user id" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":True , "message" : "id required" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error": False, "message": f"we would like to inform you {ex}", "status": 400}, status=status.HTTP_400_BAD_REQUEST)


    def changepassword(self,request):
        try:
            log.info("ApiCallController api changepassword")
            if request.data:
                user_data = User.objects.get(pk=request.data['id'])
                if user_data.is_superuser ==True and user_data.is_active == True:
                    if request.data['password'] and request.data['confirmpassword'] and 'password' in request.data:
                        pass_data = userController.UserController.changepassword(self,request,self.pass_reg)
                        if 'error' in pass_data:
                            return Response({"error":True , "message" : "please put valid password and confirmpassword and both sould match" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
                        cp_details = UserChangePasswordSerializer(user_data,data = pass_data)
                        if cp_details.is_valid():
                            obj = cp_details.save()
                            return Response({"error": False, "message": "password changed successfully", "status": 200}, status=status.HTTP_200_OK)
                    else:
                        return Response({"error":True , "message" : "password and confirmpassword required" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
                else:
                    return Response({"error":True , "message" : "you dont have authorize to change password" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error":True , "message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)


