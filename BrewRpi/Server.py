import socket
import datetime

def get_ip():
    ''' Returns the current IP address
   Helpful for Android phones :) '''
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        # doesn't even have to be reachable
        s.connect(('10.255.255.255', 1))
        IP = s.getsockname()[0]
    except:
        IP = '127.0.0.1'
    finally:
        s.close()
    return IP

def get_time():
    ''' Returns the time in desired string format '''
    return datetime.datetime.now().strftime("%Y-%m-%d at %H:%M:%S")