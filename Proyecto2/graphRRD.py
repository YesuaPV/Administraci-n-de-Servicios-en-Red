import sys
import rrdtool
import time
tiempo_actual = int(time.time())
#Grafica desde el tiempo actual menos diez minutos
tiempo_inicial = tiempo_actual - 600

ret = rrdtool.graphv( "segmentosTCP.png",
                     "--start",str(tiempo_inicial),
                     "--end","N",
                     "--vertical-label=Segmentos",
                     "--title=Segmentos TCP de un agente \n Usando SNMP y RRDtools",
#                     "DEF:sSalida=segmentosRed.rrd:segmentosSalida:AVERAGE",
#                      "VDEF:segEntradaMax=sEntrada,MAXIMUM",
#                      "CDEF:Nivel1=sSalida,1.2,LT,0,sEntrada,IF",
#                    "PRINT:segEntradaFirst:%6.2lf",
#                     "GPRINT:segEntradaDev:%6.2lf %S STDEV",
                     "LINE3:sEntrada#FF0000:Segmentros recibidos")
print(ret)