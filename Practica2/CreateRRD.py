#!/usr/bin/env python
import rrdtool
def createRRD(nombreArchivo):
    ret = rrdtool.create(nombreArchivo,
                     "--start", 'N',
                     "--step", '120',
                     "DS:pktUnicastEntrada:COUNTER:120:U:U",
                     "DS:pktEntradaIPV4:COUNTER:120:U:U",
                     "DS:ICMPechoOut:COUNTER:120:U:U",
                     "DS:sgmntRecibidos:COUNTER:120:U:U",
                     "DS:dtgUDPOut:COUNTER:120:U:U",
                     "RRA:AVERAGE:0.5:6:200",
                     "RRA:AVERAGE:0.5:1:1000")

    if ret:
        print(rrdtool.error())
        return False
    return True
