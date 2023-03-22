import os
import logging
import requests
import json

# Get an instance of a logging
log = logging.getLogger(__name__)

class OauthConnection():

    def test_connection(self, param):
        try:
            if param:
                param = json.loads(param)
                flag, response = self.make_connection(param)
                print(response)
                if flag:
                    if response.status_code == 200:
                        return (True, "Connection Successfully")
                    else:
                        return (False, "Unable to connect using given details")
                else:
                    return (False, response)

                return (False, 'Invalid parameters')
        except Exception as e:
            log.error(e)
            return (False, str(e))

    def make_connection(self,param):
        try:
            token_header={}
            token_details={
                "client_id": param['client_id'],
                "client_secret": param['client_secret'],
                "username": param['username'],
                "password":param['password'],
                "grant_type": param['grant_type'],
            }
            if len(token_header) > 0:
                response = requests.post(param['url'], header=token_header, data=json.dumps(token_details), verify=False)
            else:
                response = requests.post(param['url'], data=json.dumps(token_details), verify=False)
            return (True, response)
        except Exception as e:
            log.error(e)
            return (False, str(e))
