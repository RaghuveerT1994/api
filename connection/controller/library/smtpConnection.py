import os
import logging
import smtplib
import json
import socket

# Get an instance of a logging
log = logging.getLogger(__name__)

class SmtpConnection():

    def test_connection(self, param):
        try:
            param = json.loads(param)
            flag, response = self.make_connection(param)
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
            if param['port']:
                mailserver = smtplib.SMTP(param['hostname'],param['port'])
            else:
                mailserver = smtplib.SMTP(param['hostname'])
            # identify ourselves to smtp gmail client
            mailserver.ehlo()
            # secure our email with tls encryption
            mailserver.starttls()
            # re-identify ourselves as an encrypted connection
            mailserver.ehlo()
            status = mailserver.login(param['username'], param['password'])
            return (True, 'Successfully Connected')
        except socket.error as socketerror:
            log.error(socketerror)
            return False, "Please provide valid inputs"
        except smtplib.SMTPConnectError as e:
            log.error(e)
            print('SMTPConnectError')
            return (False, 'Unable to establish connection')
        except smtplib.SMTPHeloError as e:
            log.error(e)
            print('SMTPHeloError')
            return (False, 'Unable to establish connection')
        except smtplib.SMTPAuthenticationError as e:
            log.error(e)
            print('SMTPAuthenticationError')
            return (False, 'Invalid credentials')
        except Exception as e:
            log.error(e)
            return (False, "Please provide valid inputs")
