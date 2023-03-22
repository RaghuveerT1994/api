import logging
import requests
import json
import urllib3
import socket

from django.conf import settings

urllib3.disable_warnings()
logging.captureWarnings(True)
# Get an instance of a logging
log = logging.getLogger(__name__)

class ServicenowoauthConnection():

    def test_connection(self, param):
        try:
            if param:
                param = json.loads(param)
                if '/oauth_token.do' in param['login_url']:
                    login_url = "/".join(param["login_url"].split("/")[:-1]) + "/"
                    last_char = param['url'][-1]
                    if last_char != '/':
                        param["url"] = param["url"] + "/"
                    if login_url != param["url"]:
                        return (False, "Please provide valid url")

                    flag, response = self.make_connection(param)
                    if flag:
                        if response.status_code == 200:
                            return (True, "Connection Successfully")
                        else:
                            return (False, "Authentication Failed")
                    else:
                        return (False, response)
                else:
                    return (False, "Please provide valid login URL")

                return (False, 'Invalid parameters')
        except Exception as e:
            log.error(e)
            return (False, str(e))

    def make_connection(self,param):
        try:
            url = param['login_url']
            token_header = {
                'Content-type': 'application/x-www-form-urlencoded'
            }
            token_details={
                "client_id": param['client_id'],
                "client_secret": param['client_secret'],
                "username": param['username'],
                "password":param['password'],
                "grant_type": param['grant_type']
            }
            if len(token_header) > 0:
                response = requests.post(url, headers=token_header, data=token_details, verify=False)
            else:
                response = requests.post(url, data=json.dumps(token_details), verify=False)
            return (True, response)
        except Exception as e:
            log.error(e)
            return (False, str(e))
        except socket.error as socketerror:
            log.error(socketerror)
            return False, "Please provide valid inputs"
