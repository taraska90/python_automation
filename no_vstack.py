#-*- coding: utf-8 -*-
import datetime
import logging
import netmiko
from netmiko import ConnectHandler
import getpass
import sys


# **definition of variables**
PASSWORD = "pass"
USER = "admin"
SHOW_VS = "show vstack config"
WR_MEM = "wr mem"
logging.basicConfig(filename='main.log', level=logging.INFO)
 
with open('ip_list', 'r') as ip_list:  # Open list with mpls devices
    for ip in ip_list:
        IP = ip.rstrip()
        DEVICE_PARAMS = {'device_type': 'cisco_ios',
            'ip': IP,
            'username': USER,
            'password': PASSWORD}
        try:  # Try ssh at first
            ssh = ConnectHandler(**DEVICE_PARAMS)
            configure = ssh.send_config_from_file('no_vstack.cnf')  # File with config
            result = ssh.send_command(SHOW_VS)
            wr = ssh.send_command(WR_MEM)
            logging.info("%s %s %s" % (datetime.datetime.now(), IP, result))
        except netmiko.ssh_exception.NetMikoAuthenticationException:
            logging.info("host %s have wrong auth param" % IP)            
        except netmiko.ssh_exception.NetMikoTimeoutException:  # If ssh fail, telnet then
            logging.info("host %s don't have ssh" % IP)
            DEVICE_PARAMS = {'device_type': 'cisco_ios_telnet',
                'ip': IP,
                'username': USER,
                'password': PASSWORD}
            try:
                telnet = ConnectHandler(**DEVICE_PARAMS)
                configure = telnet.send_config_from_file('no_vstack.cnf')
                result = telnet.send_command(SHOW_VS)
                wr = telnet.send_command(WR_MEM)
                logging.info("%s %s %s" % (datetime.datetime.now(), IP, result))
            except  netmiko.ssh_exception.NetMikoAuthenticationException:
                logging.info("host %s have wrong auth param" % IP)

         
