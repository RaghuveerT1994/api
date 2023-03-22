import os
import logging
import imaplib
import json
import socket

# Get an instance of a logging
log = logging.getLogger(__name__)

class ImapConnection():

    def test_connection(self, param):
        try:
            param = json.loads(param)
            flag, login = self.make_connection(param)
            if flag:
                print(login)
                if login[0] == "OK":
                    return (True, "Connected Successfully")
                else:
                    return (False, "Connection Failed")
            else:
                return (False, str(login))
        except Exception as e:
            log.error(e)
            return (False, str(e))

    def make_connection(self, param):
        try:
            socket.setdefaulttimeout(5)
            if param['port']:
                imap_server = imaplib.IMAP4_SSL(host=param['hostname'], port=param['port'])
            else:
                imap_server = imaplib.IMAP4_SSL(host=param['hostname'])
                
            login = imap_server.login(param['username'], param['password'])
            return True, login
        except socket.error as socketerror:
            log.error(socketerror)
            return False, "Please provide valid inputs"
        except imaplib.IMAP4.error as e:
            log.error(e)
            return False, "Authentication Failed"
        except Exception as e:
            log.error(e)
            return False, "Please provide valid inputs"
