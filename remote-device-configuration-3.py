import sys
import pexpect
from netmiko import ConnectHandler

# Define variables
router = {
    'ip':"192.168.56.101",
    'username':"prne",
    'password':"cisco123!",
    'secret':"class123!",
}

# Creat ssh session
try:
   session = pexpect.spawn(f"ssh {router['username']}@{router['ip']}", encoding='utf-8', timeout=20)
   session.logfile = sys.stdout
   result = session.expect(['password:', pexpect.TIMEOUT, pexpect.EOF])
except Exception as e:
    print('--- Failure! Exception during session creation:', str(e))
    exit()
# Check the error, if exist then display the error and exit
if result != 0:
    print('--- Failer!, creating session for: ', router['ip'])
    exit()
# send the password
try:
   session.sendline(router['password'])
   result = session.expect(['#', pexpect.TIMEOUT, pexpect.EOF])
except Exception as e:
    print('--- Failure! Exception during sending password:', str(e))
    exit()    
# Check for errors entering enable mode, if exist, display it and exit
if result != 0:
    print('--- Failure!, Entering enable mode')
    exit()
# Create Netmiko connectHandler using the ssh session
device = ConnectHandler(device_type='cisco_ios', ip=router['ip'], username=router['username'], password=router['password'], secret=router['secret'])
device.enable()
# Configure OSPF
ospf_config = [
    'router ospf 1',
    'network 192.168.56.0 0.0.0.255 area 0',
    'network 192.168.57.0 0.0.0.255 area 0',
    'exit',
]
ospf_output = device.send_config_set(ospf_config)
print(ospf_output)

session.close()
