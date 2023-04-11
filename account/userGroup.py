from django.shortcuts import render

from rest_framework.response import Response
from rest_framework.viewsets import ViewSet
from rest_framework import serializers, status
from django.db.models import Q
from django.contrib.auth.models import User,Group,Permission
from django.contrib.auth import *
from account.serializers import GroupSerializer



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
                    return Response({"error" : False , "message": "group created successfully","status": 200}, status=status.HTTP_200_OK)
                else:
                    return Response({"error" : True , "message" : "group has't been created " , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error" : True , "message" : "group name is required" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error":True , "message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        

    def update(self,request):
        try:
            log.info("ApiCallController api create user group")
            if "groupId" in request.data and request.data["groupId"]:
                group = Group.objects.get(id=request.data['groupId'])
            else:
                return Response({"error" : True , "message" : "group has't been updated  groupId required" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
            if "groupName" in request.data and request.data["groupName"]:
                group.name = request.data["groupName"]
                group.save()
                return Response({"error" : False , "message": "group name updated successfully","status": 200}, status=status.HTTP_200_OK)
            else:
                return Response({"error" : True , "message" : "group has't been updated  groupname required" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            log.error(ex)
            return Response({"error":True , "message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)

    def delete(self,request):
        try:
            log.info("ApiCallController api create user group")
            if "groupId" in request.data and request.data["groupId"]:
                unused_group = Group.objects.get(id=request.data["groupId"],is_deleted=False)
                active_group_user = unused_group.user_set.all()
                print(unused_group)
                if active_group_user:
                    return Response({"error":True , "message" : "some user still mapped to the group" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
                if unused_group:
                        del_group = {
                            "is_deleted":"True"
                        }
                        datas = GroupSerializer(unused_group,data=del_group,partial=True)
                        if datas.is_valid():
                            obj = datas.save()
                            return Response({"error" : False , "message": "group deleted successfully","status": 200}, status=status.HTTP_200_OK)
                else:
                    return Response({"error":True , "message" : "please provide existing group id " , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":True , "message" : "please provide existing group id " , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error":True , "message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)

    def list(self,request):
        try:
            log.info("ApiCallController api create user group")
            datas=Group.objects.filter(is_deleted=False).values()
            print(datas)
            if datas:
                return Response({"error" : False , "message": "successfully","status": 200,"data":datas}, status=status.HTTP_200_OK)
            else:
                return Response({"error":True , "message" : "failed to fatch data" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as ex:
            log.error(ex)
            return Response({"error":True , "message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        

    def view(self,request):
        try:
            log.info("ApiCallController api create user group")
            if request.data["groupId"] and "groupId" in request.data:
                try:
                    datas=Group.objects.filter(id=request.data["groupId"],is_deleted=False).values()
                    if datas:
                        return Response({"error" : False , "message": "successfull","status": 200,"data":datas}, status=status.HTTP_200_OK)
                    else:
                        return Response({"error":True , "message" : "please provide existing group id " , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)

                except Group.DoesNotExist:
                    return Response({"error":True , "message" : "please provide existing group id " , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({"error":True , "message" : "please provide existing group id " , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error":True , "message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)

    def addToGroup(self,request):
        try:
            log.info("ApiCallController api assign user group")
            group =Group.objects.get(id=request.data["groupId"],is_deleted=False)
            user = User.objects.get(id=request.data["userId"],is_deleted=False)
            if group and user:
                user.groups.add(group)
                return Response({"error" : False , "message": "user added successfully to the group","status": 200}, status=status.HTTP_200_OK)
            return Response({"error":True , "message" : "failed : user not added to the group" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error":True , "message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)


    def removeGroup(self,request):
        try:
            log.info("ApiCallController api revoke user group")
            group =Group.objects.get(id=request.data["groupId"],is_deleted=False)
            user = User.objects.get(id=request.data["userId"],is_deleted=False)
            if group and user:
                user.groups.remove(group)
                return Response({"error" : False , "message": "user successfully removed from the group","status": 200}, status=status.HTTP_200_OK)
            return Response({"error":True , "message" : "failed : user not removed from the group" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as ex:
            log.error(ex)
            return Response({"error":True , "message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)


    def listOfGroupByUser(self,request):
            try:
                log.info("ApiCallController api revoke user group")
                user = User.objects.get(id=request.data["userId"],is_deleted=False)
                allGroups=user.groups.all()
                if allGroups:
                    return Response({"error" : False , "message": "successful","status": 200,"data":allGroups.values()}, status=status.HTTP_200_OK)
                return Response({"error":True , "message" : "failed : user not assign to any group" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)
            except Exception as ex:
                log.error(ex)
                return Response({"error":True , "message" : f"we would like to inform you {ex}" , "status" : 400}, status=status.HTTP_400_BAD_REQUEST)

   

    





