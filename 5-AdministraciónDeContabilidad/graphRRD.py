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
                     "DEF:sEntrada=segmentosRed.rrd:segmentosEntrada:AVERAGE",
                     "DEF:sSalida=segmentosRed.rrd:segmentosSalida:AVERAGE",
                     "VDEF:segEntradaDev=sEntrada,STDEV",
                      "VDEF:segEntradaLast=sEntrada,LAST",
                      "VDEF:segEntradaFirst=sEntrada,FIRST",
                      "VDEF:segEntradaMax=sEntrada,MAXIMUM",
                      "CDEF:Nivel1=sSalida,1.2,LT,0,sEntrada,IF",
                      "PRINT:segEntradaLast:%6.2lf",
                      "PRINT:segEntradaFirst:%6.2lf",
                     "GPRINT:segEntradaMax:%6.2lf %S segEntMAX",
                     "GPRINT:segEntradaDev:%6.2lf %S STDEV",
                     "LINE3:sEntrada#FF0000:Segmentros recibidos",
                     "LINE2:sSalida#0000FF:Segmentos enviados",
                     "AREA:Nivel1#00FF00:Nivel 1" )
print(ret)