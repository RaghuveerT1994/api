
from django.contrib.auth.models import User,Group
from rest_framework import serializers

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
        fields=("id","is_active","is_deleted")

class UserChangePasswordSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
        model=User
        fields=("id","password")

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta():
        model=Group
        fields=("id","name","description","extras","isActive","is_deleted")
 