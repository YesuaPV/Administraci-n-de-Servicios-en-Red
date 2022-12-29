from pysnmp.hlapi import *

def consulta(ip,comunidad,OID):
    iterator = getCmd(
        SnmpEngine(),
        CommunityData(comunidad, mpModel=0),
        UdpTransportTarget((ip, 161)),
        ContextData(),
        ObjectType(ObjectIdentity(OID))
    )

    errorIndication, errorStatus, errorIndex, varBinds = next(iterator)

    if errorIndication:
        print(errorIndication)

    elif errorStatus:
        print('%s at %s' % (errorStatus.prettyPrint(),
                            errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
    else:
        texto = ""
        for varBind in varBinds:
            texto = texto + (' = '.join([x.prettyPrint() for x in varBind]))
        return texto.split("= ")[1]

#MAIN
ip = '10.100.72.13'
# ip = '10.100.74.190'
comunidad = 'ComunidadASRErick'
OID = {
    'c1': '1.3.6.1.2.1.2.2.1.18.',
    'c2': '1.3.6.1.2.1.4.10.0',
    'c3': '1.3.6.1.2.1.5.1.0',
    'c4': '1.3.6.1.2.1.6.12.0',
    'c5': '1.3.6.1.2.1.7.4.0'
}

print("Consultas realizadas IP " + ip)
print("Nombre de la comunidad: " + comunidad)
print("Ejercicios (3)\n")

print("1) Paquetes multicast que han enviado las primeras 5 interfaces: ")
for i in range(5):
    print("Interfaz " + str(i+1) + ": " + consulta(ip,comunidad,OID.get('c1')+str(i+1)))

print("2) Paquetes IPV4 que los protocolos locales de usuarios IPV4 suministraron a IPV4 en las solicitudes"
      " de transmisión: " + consulta(ip,comunidad,OID.get('c2')))
print("3) Mensajes ICMP que ha recibido el agente: " + consulta(ip,comunidad,OID.get('c3')))
print("4) Segmentos retransmitidos, es decir, el número de segmentos TCP transmitidos que contienen uno o"
      " más octetos transmitidos previamente: " + consulta(ip,comunidad,OID.get('c4')))
print("5) Datagramas enviados por el dispositivo: " + consulta(ip,comunidad,OID.get('c5')))
