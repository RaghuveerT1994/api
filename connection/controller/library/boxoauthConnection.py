# importing necessary libraries

import logging
import requests
import json



# Get an instance of a logging
log = logging.getLogger(__name__)

class InvalidCredentials(Exception):
    pass

class BoxoauthConnection():

    def test_connection(self, params):
        try:
            print("=====inside box =====")

            params=json.loads(params,strict=False)
            print(params)
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
            grant_type=params["grant_type"]
            client_id=params["client_id"]
            client_secret=params["client_secret"]
            url = params["token_uri"]
            refresh_token=params["refresh_token"]
            payload='grant_type=%s&client_id=%s&client_secret=%s&refresh_token=%s'%(grant_type,client_id,client_secret,refresh_token)
            headers = {
                'Content-Type': 'application/x-www-form-urlencoded',
                'Cookie': 'box_visitor_id=6310e6ab3b1d06.15435778; site_preference=desktop'
                }

            response = requests.request("POST", url, headers=headers, data=payload)

            print(response.text)

            data=response.json()
          
            #r.account_id,response.status_code==200
            print(response.status_code)
            if response.status_code==400:
                raise InvalidCredentials
            elif response.status_code==200:

                if data["access_token"]:
                    print("success")
                    url = "https://api.box.com/2.0/folders/0/items"

                    payload={}
                    headers = {
                    'Authorization': 'Bearer %s'%(data["access_token"])
                    }

                    response = requests.request("GET", url, headers=headers, data=payload)

                    print(response.text)

                    return response,{"message":"Success"}
               
            else:
                raise InvalidCredentials
        except InvalidCredentials:
            return False, {"message":"Invalid credentials"}
        except Exception as e:
            log.error(e)
            return False, {"message":str(e)}

