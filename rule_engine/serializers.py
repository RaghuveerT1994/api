import os
from django.conf import settings
from django.db import models
from django.db.models import Q, fields
from django.contrib.auth.models import User

from rest_framework import serializers

from rule_engine.models import TBLRules, CommonMaster, TBLRulesSet

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

class userSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
        model=User
        fields=("username","first_name", "last_name","email","password","is_staff","is_active","is_superuser")
   
    
class userShowSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
        model=User
        fields=("id","username","first_name", "last_name","email","is_staff","is_active","is_superuser")

class userDeleteSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
        model=User
        fields=("id","is_active")

class UserChangePasswordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
        model=User
        fields=("id","password")
 