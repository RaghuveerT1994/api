from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from django.db.models import Q
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth import *



import logging
import datetime

log = logging.getLogger(__name__)
pattern = "\W"



class UserGroupsView(ViewSet):

    def create(self,request):
        try:
            log.info("ApiCallController api create user group")
            if "name" in request.data and request.data["name"]:
                new_group = Group.objects.create(name=request.data["name"])

                ##for adding permission for group
                # if "permission_id_list" in request.data and request.data["permission_id_list"]:
                #     for id in request.data['permission_id_list']:
                #         permission = Permission.objects.filter(id=id).first()
                #         new_group.permissions.add(permission)
                
                new_group.save()
                if new_group:
                    return Response({"error" : False , "Message": "group created successfully","status": 200}, status=status.HTTP_200_OK)
                else:
                    return Response({"error" : True , "Message" : "group has't been created " , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error" : True , "Message" : "group name is required" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error":True , "Message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        

    def update(self,request):
        try:
            log.info("ApiCallController api create user group")
            if "groupId" in request.data and request.data["groupId"]:
                group = Group.objects.get(id=request.data['groupId'])
            else:
                return Response({"error" : True , "Message" : "group has't been updated  groupId required" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)

            if "groupName" in request.data and request.data["groupName"]:
                group.name = request.data["groupName"]
                group.save()
                return Response({"error" : False , "Message": "group name updated successfully","status": 200}, status=status.HTTP_200_OK)
            else:
                return Response({"error" : True , "Message" : "group has't been updated  groupname required" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            log.error(ex)
            return Response({"error":True , "Message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:
            log.info("ApiCallController api create user group")
            if "groupId" in request.data and request.data["groupId"]:
                unused_group = Group.objects.get(id=request.data["groupId"])
                unused_group.delete()
                return Response({"error" : False , "Message": "group deleted successfully","status": 200}, status=status.HTTP_200_OK)
            else:
                return Response({"error":True , "Message" : "please provide existing group id " , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        
        except Exception as ex:
            log.error(ex)
            return Response({"error":True , "Message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        try:
            log.info("ApiCallController api create user group")
            datas=Group.objects.filter().values()
            print(datas)
            if datas:
                return Response({"error" : False , "Message": "successfully","status": 200,"data":datas}, status=status.HTTP_200_OK)
            else:
                return Response({"error":True , "Message" : "failed to fatch data" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            log.error(ex)
            return Response({"error":True , "Message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        

    def view(self,request):
        try:
            log.info("ApiCallController api create user group")
            if request.data["groupId"] and "groupId" in request.data:
                try:
                    datas=Group.objects.filter(id=request.data["groupId"]).values()
                    if datas:
                        return Response({"error" : False , "Message": "successfull","status": 200,"data":datas}, status=status.HTTP_200_OK)
                    else:
                        return Response({"error":True , "Message" : "please provide existing group id " , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)

                except Group.DoesNotExist:
                    return Response({"error":True , "Message" : "please provide existing group id " , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":True , "Message" : "please provide existing group id " , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error":True , "Message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)

    def addToGroup(self,request):
        try:
            log.info("ApiCallController api assign user group")
            group =Group.objects.get(id=request.data["groupId"])
            user = User.objects.get(id=request.data["userId"])
            if group and user:
                user.groups.add(group)
                return Response({"error" : False , "Message": "user added successfully to the group","status": 200}, status=status.HTTP_200_OK)
            return Response({"error":True , "Message" : "failed : user not added to the group" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error":True , "Message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)


    def removeGroup(self,request):
        try:
            log.info("ApiCallController api revoke user group")
            group =Group.objects.get(id=request.data["groupId"])
            user = User.objects.get(id=request.data["userId"],)
            if group and user:
                user.groups.remove(group)
                return Response({"error" : False , "Message": "user successfully removed from the group","status": 200}, status=status.HTTP_200_OK)
            return Response({"error":True , "Message" : "failed : user not removed from the group" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error":True , "Message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)


        

    





