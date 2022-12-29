import sys
import rrdtool
import time
from ControladorBDD import file_exist

def grafica(agente, iniTime, finTime):
    archivo = "RRDTools/" + agente.get('ip') + '_' + agente.get('comunidad') + ".rrd"
    if iniTime > finTime:
        iniTime, finTime = finTime, iniTime
    tiempo_actual = finTime
    tiempo_inicial = iniTime

    if not file_exist(archivo):
        return False

    ret1 = rrdtool.graphv( "images/Unicast.png",
                         "--start",str(tiempo_inicial),
                         "--end",str(tiempo_actual),
                         "--vertical-label=Paquetes",
                         "--title=Paquetes unicast de entrada \n Usando SNMP y RRDtools",
                         "DEF:pktIn=" + archivo + ":pktUnicastEntrada:AVERAGE",
                         "LINE3:pktIn#00FF00:Segmentros recibidos")

    ret2 = rrdtool.graphv("images/IPV4.png",
                         "--start", str(tiempo_inicial),
                         "--end", str(tiempo_actual),
                         "--vertical-label=Mensajes",
                         "--title=Paquetes IPV4 de entrada \n Usando SNMP y RRDtools",
                         "DEF:pktInIPV4=" + archivo + ":pktEntradaIPV4:AVERAGE",
                         "LINE3:pktInIPV4#00FF00:Mensajes evniados")
    ret3 = rrdtool.graphv("images/ICMP.png",
                         "--start", str(tiempo_inicial),
                         "--end", str(tiempo_actual),
                         "--vertical-label=Paquetes",
                         "--title=Mensajes ICMP echo enviados\n Usando SNMP y RRDtools",
                         "DEF:ICMPout=" + archivo + ":ICMPechoOut:AVERAGE",
                         "LINE3:ICMPout#00FF00:Paquetes recibidos")
    ret4 = rrdtool.graphv("images/TCP.png",
                         "--start", str(tiempo_inicial),
                         "--end", str(tiempo_actual),
                         "--vertical-label=Segmentos",
                         "--title=Segmentos recibidos \n Usando SNMP y RRDtools",
                         "DEF:sgmntIn=" + archivo + ":sgmntRecibidos:AVERAGE",
                         "LINE3:sgmntIn#00FF00:Segmentos recibidos")
    ret5 = rrdtool.graphv("images/UDP.png",
                         "--start", str(tiempo_inicial),
                         "--end", str(tiempo_actual),
                         "--vertical-label=Paquetes",
                         "--title=Datagramas entregados \n Usando SNMP y RRDtools",
                         "DEF:dtgOut=" + archivo + ":dtgUDPOut:AVERAGE",
                         "LINE3:dtgOut#00FF00:Datagramas entregados")

    print(ret1)
    print(ret2)
    print(ret3)
    print(ret4)
    print(ret5)

    return True