import os
import logging

from connection.models import ConnectionType

from connection.controller.connectionController import ConnectionController

# Get an instance of a logging
log = logging.getLogger(__name__)

def test_connection(request):
    try:
        if 'connection_type_id' in request.data:
            connection_type_obj = ConnectionType.objects.get(connection_type_id=request.data['connection_type_id'])
            try:
                connect= ConnectionController()
                return connect.test_connection(connection_type_obj.connection_type_code,connection_type_obj.application_code,request.data['parameter'])
            except ConnectionType.DoesNotExist:
                log.error("No connection type for requested id: "+str(request.data['connection_type_id']))
                pass
            return (True, 'Connected Successfully')
        return (False, 'Invalid connection type')
    except Exception as e:
        log.error(e)
        return (False, str(e))
