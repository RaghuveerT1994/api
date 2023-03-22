# importing necessary libraries
import dropbox

import logging
import requests
import json


# Get an instance of a logging
log = logging.getLogger(__name__)

class DropboxoauthConnection():

    def test_connection(self, params):
        try:
            print("=====inside dropbox drive=====")
            #The control character can be allowed inside a string as follows,

            params=json.loads(params,strict=False)
            if params:
                service,resp= self.make_connection(params)
                if resp=="Success":
            
                    return service, resp
                    
                else:
                    return None, resp

            return (False, 'Invalid parameters')
        except Exception as e:
            log.error(e)
            return (False, str(e))

    def make_connection(self,params):

        try:
            refresh_token=params["refresh_token"]
            refresh_url=params["refresh_url"]
            grant_type=params["grant_type"]
            authorization_code=params["authorization"]
          

            payload='refresh_token=%s&grant_type=%s'%(refresh_token,grant_type)
            auth_code='Basic %s'%(authorization_code)
            
            headers = {
            'Authorization': auth_code,
            'Content-Type': 'application/x-www-form-urlencoded'
            }
         
            response = requests.request("POST", refresh_url, headers=headers, data=payload)
            
            data=response.json()
          
            dbx = dropbox.Dropbox(data["access_token"])
          
            result=dbx.users_get_current_account()
            #r.account_id,response.status_code==200

            if result.account_id:
                print("success")
                # response = requests.post(param['url'], header=token_header, data=json.dumps(token_details), verify=False)
                return (True, "Success")
               
            else:
                print("failed")
                return (False , "Unable to connect")
            
        except Exception as e:
            log.error("failed")
            log.error(e)
            return (False, str(e))

