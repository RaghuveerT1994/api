from rest_framework.response import Response
from rest_framework import status
import datetime
from django.contrib.auth.hashers import make_password
import re

import logging
import datetime

log = logging.getLogger(__name__)
pattern = "\W"


class UserController():

    def updateUserDetails(self,request):
        try:
            log.info("ApiCallController api updateDetails")
            new_data={}
            if request.data:
                if 'first_name' in request.data and request.data['first_name']:
                    new_data['first_name'] = request.data['first_name']
                # else:
                #     return {"error": True, "message": "please provide first_name", "status": 400}
                if 'last_name' in request.data and request.data['last_name']:
                    new_data['last_name'] = request.data['last_name']
                # else:
                #     return {"error": True, "message": "please provide last_name", "status": 400}
                if 'is_staff' in request.data and request.data['is_staff']:
                    new_data['is_staff'] = request.data['is_staff'] 
                # else:
                #     return {"error": True, "message": "please provide is_staff", "status": 400}
                if 'is_active' in request.data and request.data['is_active']:  
                    new_data['is_active'] = request.data['is_active'] 
                # else:
                #     return {"error": True, "message": "please provide is_active", "status": 400}
                if 'is_superuser' in request.data and request.data['is_superuser']:  
                    new_data['is_superuser'] = request.data['is_superuser'] 
                # else:
                #     return {"error": True, "message": "please provide is_superuser", "status": 400}
                return (new_data)
            else:
                return {"error": True, "message": "please provide details", "status": 400}
        except Exception as ex:
            log.error(ex)
            return {"error": True, "message": f"Exception please provide details {ex}", "status": 400}
        
    def changepassword(self,request,pass_reg): 
        try:
            log.info("ApiCallController api passwordDetails")
            pass_data={}
            if request.data:
                if 'password' in request.data and request.data['password']:
                        valid = re.compile(pass_reg)
                        if (request.data['password'] == request.data['confirmpassword'] and re.search(valid,request.data['password'])):
                            print('before password assign')
                            pass_data['password'] = make_password(request.data['password'])
                            print("before controller successfulv return")
                            return pass_data
                        else:
                            print("password not match inside else")
                            return {"error": True, "message": " please put valid password and confirm password", "status": 400}
                else:
                    return {"error": True, "message": "please provide password", "status": 400}
            else:
                return {"error": True, "message": "please provide password", "status": 400}
        except Exception as ex:
            log.error(ex)
            return {"error": True, "message": f"Exception please provide valid details {ex}", "status": 400}