import logging
from django.http import response
import requests
import json
import urllib3
import socket
import pyodbc
import pandas as pd
from django.conf import settings

urllib3.disable_warnings()
logging.captureWarnings(True)
# Get an instance of a logging
log = logging.getLogger(__name__)

class MssqloauthConnection():

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
            server =  param['hostname'] + "," + param['port']
            response_data = {}
            response_data['status'] = "Failed"
            db_connection = pyodbc.connect(
                'DRIVER={ODBC Driver 17 for SQL Server}' + 
                ';SERVER=' + server + ';UID=' + param['username'] + 
                ';PWD=' + param['password'] +
                ';database=' +param['database_name'] +
                ';TrustServerCertificate=YES' +
                ';Trusted_Connection=no;'
                )
            df = pd.read_sql("SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE IN ('VIEW', 'BASE TABLE')", db_connection)
            print(df)
            if not df.empty:
                response_data['status'] = "OK"
            else:
                response_data['status'] = "Database Not Found"
            return (True, response_data)
        except Exception as e:
            log.error(e)
            return False, "Authentication Failed"
        except pyodbc.InternalError as inerr: 
            log.error(inerr)
            return False, "Authentication Failed"  
        except pyodbc.OperationalError as operr:
            log.error(operr)
            return False, "Authentication Failed" 
        except socket.error as socketerror:
            log.error(socketerror)
            return False, "Please provide valid inputs"
