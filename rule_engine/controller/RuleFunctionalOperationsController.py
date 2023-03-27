from rest_framework.response import Response
from rest_framework import status
import datetime
from django.contrib.auth.hashers import make_password
import re

import logging
import datetime

log = logging.getLogger(__name__)
pattern = "\W"


class RuleFunctionalOperationsController():

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
                if 'created_at' in request.data and request.data['created_at']:  
                    new_data['created_at'] = request.data['created_at'] 
                # else:
                #     return {"error": True, "message": "please provide is_superuser", "status": 400}
                if 'updated_user' in request.data and request.data['updated_user']:  
                    new_data['updated_user'] = request.data['updated_user'] 
                # else:
                #     return {"error": True, "message": "please provide is_superuser", "status": 400}
                if 'updated_at' in request.data and request.data['updated_at']:  
                    new_data['updated_at'] = request.data['updated_at'] 
                # else:
                #     return {"error": True, "message": "please provide is_superuser", "status": 400}
                return (new_data)
            else:
                return {"error": True, "message": "please provide details", "status": 400}
        except Exception as ex:
            log.error(ex)
            return {"error": True, "message": f"Exception please provide details {ex}", "status": 400}
        