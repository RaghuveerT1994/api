import os
import logging
import poplib
import ssl
import json
import socket

# Get an instance of a logging
log = logging.getLogger(__name__)

class Pop3Connection():

    def test_connection(self, param):
        try:
            param = json.loads(param)
            flag, response, data, octets = self.make_connection(param)
            if flag:
                print(response)
                return (True, "Connected Successfully")
            else:
                return (False, str(response))
        except Exception as e:
            log.error(e)
            return (False, str(e))

    def make_connection(self, param):
        try:
            socket.setdefaulttimeout(5)
            context = ssl.SSLContext(ssl.PROTOCOL_TLS)
            context.set_ciphers('DEFAULT:@SECLEVEL=1')

            if param['port']:
                pop_server = poplib.POP3_SSL(param['hostname'], port=param['port'], context=context)
            else:
                pop_server = poplib.POP3_SSL(param['hostname'], context=context)
            pop_server.user(param['username'])
            pop_server.pass_(param['password'])

            response, data, octets = pop_server.uidl()  # uid number
            return (True, response, data, octets)
        except socket.error as socketerror:
            log.error(socketerror)
            return (False, "Please provide valid inputs", '', '')
        except poplib.error_proto as e:
            log.error(e)
            return (False, "Authentication Failed", '', '')
        except Exception as e:
            log.error(e)
            return (False, "Please provide valid inputs", '', '')
