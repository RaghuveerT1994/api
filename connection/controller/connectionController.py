import json
import logging
import os
import importlib

""" Import Django libraries """
from django.conf import settings

# Get an instance of a logging
log = logging.getLogger(__name__)

class ConnectionController():

    def test_connection(self, code, application_code, param):
        try:
            if param:
                class_file_name = code
                if code == 'oauth':
                    class_file_name = application_code + code

                if os.path.exists(os.path.join(settings.BASE_DIR,'connection/controller/library/'+class_file_name+'Connection.py')):
                    classname = str(class_file_name.capitalize())+'Connection'
                    module = importlib.import_module('connection.controller.library.'+class_file_name+'Connection')
                    if module:
                        connection= getattr(module, classname)
                        if connection:
                            connection_obj = connection()
                            return connection_obj.test_connection(param)
                        return (False, "Invalid connection")
            return (False, "Invalid parameter")
        except Exception as e:
            log.error(e)
            return (False, str(e))
