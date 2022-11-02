#!/usr/bin/env python
import rrdtool
def createRRD(nombreArchivo):

    ret = rrdtool.create(nombreArchivo,
                     "--start", 'N',
                     "--step", '60',
                     "DS:pktUnicastEntrada:COUNTER:120:U:U",
                     "DS:pktEntradaIPV4:COUNTER:120:U:U",
                     "RRA:AVERAGE:0.5:6:5",
                     "RRA:AVERAGE:0.5:1:20")

    if ret:
        print(rrdtool.error())
        return False
    return True
