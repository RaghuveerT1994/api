from email import message
import os
import logging
import requests
import json

from googleapiclient.discovery import build
import io
from apiclient import http
from google.oauth2 import service_account

# Get an instance of a logging
log = logging.getLogger(__name__)

class GoogledriveoauthConnection():

    def test_connection(self, params):
        try:
            print("inside google drive")
            #The control character can be allowed inside a string as follows,

            params=json.loads(params,strict=False)
          
            if params:
                service,resp= self.make_connection(params)
                if resp["message"]=="Success":
            
                    return service,resp
                    
                else:
                    return None,resp

                return (False, 'Invalid parameters')
        except Exception as e:
            log.error(e)
            return (False, {"message":str(e)})

    def make_connection(self,params):
        try:
            credentials = service_account.Credentials.from_service_account_info(params)
            service = build('drive', 'v3', credentials=credentials)
            if service:
                print("success")
                # response = requests.post(param['url'], header=token_header, data=json.dumps(token_details), verify=False)
                return service,{"message":"Success"}
               
            else:
                print("failed")
                return None
            
        except Exception as e:
            log.error(e)
            return False, {"message":str(e)}
