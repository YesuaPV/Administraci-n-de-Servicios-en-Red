import time
import rrdtool
from getSNMP import consultaSNMP


def update(archivo):
    while 1:
        uncst_in_pkt = int(
            consultaSNMP('comunidadYesua', '10.0.2.15',
                         '1.3.6.1.2.1.2.2.1.11.2'))
        pkt_in = int(
            consultaSNMP('comunidadYesua', '10.0.2.15',
                         '1.3.6.1.2.1.4.3.0'))
        valor = "N:" + str(uncst_in_pkt) + ':' + str(pkt_in)
        print(valor)
        rrdtool.update(archivo, valor)
        # rrdtool.dump('traficoRED.rrd','traficoRED.xml')
        time.sleep(1)

    if ret:
        print(rrdtool.error())
        time.sleep(300)
