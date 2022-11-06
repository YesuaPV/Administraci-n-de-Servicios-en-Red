import time
import rrdtool
from getSNMP import consultaSNMP
from ControladorBDD import file_exist
from CreateRRD import createRRD


def update(agente):
    archivo = "RRDTools/"+agente.get('ip')+'_'+agente.get('comunidad')+".rrd"
    if not file_exist(archivo):
        if not createRRD(archivo):
            return False

    while 1:
        uncst_in_pkt = int(consultaSNMP(agente, '1.3.6.1.2.1.2.2.1.11.2'))
        pkt_in = int(consultaSNMP(agente, '1.3.6.1.2.1.4.3.0'))
        ICMP_out = int(consultaSNMP(agente, '1.3.6.1.2.1.5.21.0'))
        sgmnt_in = int(consultaSNMP(agente, '1.3.6.1.2.1.6.10.0'))
        dtg_out = int(consultaSNMP(agente, '1.3.6.1.2.1.7.1.0'))
        valor = "N:" + str(uncst_in_pkt) + ':' + str(pkt_in) + ':' + str(ICMP_out) + ':' + str(sgmnt_in) + ':' + str(dtg_out)
        print(valor)
        rrdtool.update(archivo, valor)
        time.sleep(1)

    if ret:
        print(rrdtool.error())
        time.sleep(300)