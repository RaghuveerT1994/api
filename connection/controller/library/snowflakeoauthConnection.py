import logging
from django.http import response
import requests
import json
import urllib3
import socket
import snowflake.connector
import pandas as pd
from django.conf import settings

urllib3.disable_warnings()
logging.captureWarnings(True)
# Get an instance of a logging
log = logging.getLogger(__name__)

class SnowflakeoauthConnection():

    def test_connection(self, param):
        try:
            param = json.loads(param)
            flag, login = self.make_connection(param)
            if flag:
                if login['status'] == "OK":
                    return (True, "Connected Successfully")
                else:
                    return (False, "Connection Failed")
            else:
                return (False, str(login))
        except Exception as e:
            log.error(e)
            return (False, str(e))

    def make_connection(self,param):
        try:
            response_data = {}
            response_data['status'] = "Failed"

            db_connection = snowflake.connector.connect(
                            user=param['username'],
                            password=param['password'] ,
                            account=param['account_name'] ,
                            database=param['database_name'] ,
                            schema=param['schema']
            )
            df = pd.read_sql("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE IN ('VIEW', 'BASE TABLE') and TABLE_SCHEMA = 'PUBLIC'", db_connection)
            print(df)
            if not df.empty:
                response_data['status'] = "OK"
            else:
                response_data['status'] = "Database Not Found"
            return (True, response_data)
        except Exception as e:
            log.error(e)
            return False, "Authentication Failed"
        except socket.error as socketerror:
            log.error(socketerror)
            return False, "Please provide valid inputs"
