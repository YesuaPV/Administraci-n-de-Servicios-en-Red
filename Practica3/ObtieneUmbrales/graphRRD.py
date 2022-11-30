import sys
import rrdtool
import time

rrdpath = '/home/linuxlite/PycharmProjects/Administraci-n-de-Servicios-en-Red/Practica3/ObtieneUmbrales/'
ultima_lectura = int(rrdtool.last(rrdpath + "promedio.rrd"))
tiempo_final = ultima_lectura
tiempo_inicial = tiempo_final - 16000

ret1 = rrdtool.graphv( "CPU.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label=Porcentaje",
                     "--title= CPU load",
                     "DEF:CPUload=promedio.rrd:CPUload:AVERAGE",
                     "LINE1:CPUload#00FF00:CpuLoad")

ret2 = rrdtool.graphv( "RAM.png",
                     "--start",str(tiempo_inicial),
                     "--end",str(tiempo_final),
                     "--vertical-label=Porcentaje",
                     "--title= RAMload",
                     "DEF:RAMload=promedio.rrd:RAMload:AVERAGE",
                     "LINE1:RAMload#00FF00:RamLoad")
ret3 = rrdtool.graphv("RED.png",
                     "--start", str(tiempo_inicial),
                     "--end", str(tiempo_final),
                     "--vertical-label=KiloBytes",
                     "--title=Trafico de RED",
                     "DEF:InOctets=promedio.rrd:InOctets:AVERAGE",
                     "DEF:OutOctets=promedio.rrd:OutOctets:AVERAGE",
                     "LINE1:InOctets#00FF00:Entrada",
                     "LINE1:OutOctets#FF0000:Salida")

print(ret1)
print(ret2)
print(ret3)
