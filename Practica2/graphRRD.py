import sys
import rrdtool
import time

def grafica(archivo):
    tiempo_actual = int(time.time())
    tiempo_inicial = tiempo_actual - 600

    ret = rrdtool.graphv( "Unicast.png",
                         "--start",str(tiempo_inicial),
                         "--end","N",
                         "--vertical-label=Paquetes",
                         "--title=Paquetes unicast de entrada \n Usando SNMP y RRDtools",
                         "DEF:pktIn=" + archivo + ":pktUnicastEntrada:AVERAGE",
    #                      "VDEF:segEntradaMax=sEntrada,MAXIMUM",
    #                      "CDEF:Nivel1=sSalida,1.2,LT,0,sEntrada,IF",
    #                    "PRINT:segEntradaFirst:%6.2lf",
    #                     "GPRINT:segEntradaDev:%6.2lf %S STDEV",
                         "LINE3:pktIn#FF0000:Segmentros recibidos")

    ret = rrdtool.graphv("IPV4.png",
                         "--start", str(tiempo_inicial),
                         "--end", "N",
                         "--vertical-label=Paquetes",
                         "--title=Paquetes IPV4 de entrada \n Usando SNMP y RRDtools",
                         "DEF:pktIn=" + archivo + ":pktEntradaIPV4:AVERAGE",
                         "LINE3:pktIn#FF0000:Segmentros recibidos")
    print(ret)