import netmiko
from netmiko import ConnectHandler
import pexpect
# Define variables
router = {
    'ip_address':"192.168.56.101",
    'username':"prne",
    'password':"cisco123!",
    'password_enable':"class123!",
}

# Creat ssh session
session = pexpect.spawn('ssh ' + 'username' + '@' + 'ip_address', encoding='utf-8', timeout=20)
result = session.expect(['password:', pexpect.TIMEOUT, pexpect.EOF])
# Check the error, if exist then display the error and exit
if result != 0:
    print('--- Failer!, creating session for: ', 'ip_address')
    exit()
# Contact to the router
R1 = device
device = ConnectHandler(**router)
device.enable()
session.sendline('enable')
result = session.expect(['Password:', pexpect.TIMEOUT, pexpect.EOF])
# check for error if exit display the error and exit
if result != 0:
    print('--- failure! entering enable mode')
    exit=()
with ConnectHandler(**R1) as net_connect:
    net_connect.enable()   
ospf_config = [
    'router ospf 1',
    'network 192.168.56.101 255.255.255.0 area 0 '
    'network 192.168.57.101 255.255.255.0 area 0',
    'exit',
]

ospf_output = device.send_config_set(ospf_config)
print(ospf_output)

# Disconnect from the router
device.disconnect()
