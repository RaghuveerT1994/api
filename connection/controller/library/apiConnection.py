import os
import logging
import request

# Get an instance of a logging
log = logging.getLogger(__name__)

class ApiConnection():

    def test_connection(self, param):
        try:
            return (True, "Connected Successfully")
        except Exception as e:
            log.error(e)
            return (False, str(e))

    def make_connection(self,param):
        try:
            pass
        except Exception as e:
            pass
