# from pysnmp.hlapi import *
import os

import pyautogui
#
# iterator = getCmd(
#     SnmpEngine(),
#     CommunityData('comunidadASRWin', mpModel=0),
#     UdpTransportTarget(('192.168.0.191', 161)),
#     ContextData(),
#     ObjectType(ObjectIdentity('1.3.6.1.2.1.2.2.2.1'))
# )
#
# errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
#
# if errorIndication:
#     print(errorIndication)
#
# elif errorStatus:
#     print('%s at %s' % (errorStatus.prettyPrint(),
#                         errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
#
# else:
#     for varBind in varBinds:
#         # print(' = '.join([x.prettyPrint() for x in varBind]))
#       print(varBind)
#       # var = str(varBind)
#       # splited = var[var.index('x')+1:len(var)]
#       # print(bytes.fromhex(splited).decode('utf-8'))

print("hola")
input()
pyautogui.hotkey('ctrl','l')
print("hola2")