import time
import rrdtool
from getSNMP import consultaSNMP
rrdpath = '/home/linuxlite/PycharmProjects/Administraci-n-de-Servicios-en-Red/Practica3/ObtieneUmbrales/'
carga_CPU = 0

while 1:
    carga_CPU1 = int(consultaSNMP('comunidadYesua', 'localhost', '1.3.6.1.2.1.25.3.3.1.2.196608'))
    carga_CPU2 = int(consultaSNMP('comunidadYesua', 'localhost', '1.3.6.1.2.1.25.3.3.1.2.196609'))
    carga_CPU = (carga_CPU2 + carga_CPU1) / 2
    ram_Total = int(consultaSNMP('comunidadYesua', 'localhost', '1.3.6.1.4.1.2021.4.5.0'))
    ram_disp = int(consultaSNMP('comunidadYesua', 'localhost', '1.3.6.1.4.1.2021.4.11.0'))
    carga_RAM = (ram_Total-ram_disp)/(ram_Total)*100
    inKB = int(int(consultaSNMP('comunidadYesua', 'localhost', '1.3.6.1.2.1.2.2.1.10.2'))/1024)
    outKB = int(int(consultaSNMP('comunidadYesua', 'localhost', '1.3.6.1.2.1.2.2.1.16.2'))/1024)
    valor = "N:" + str(carga_CPU) + ':' + str(carga_RAM) + ':' + str(inKB) + ':' + str(outKB)
    print (valor)
    rrdtool.update(rrdpath+'promedio.rrd', valor)
    time.sleep(.25)

if ret:
    print (rrdtool.error())
    time.sleep(300)
