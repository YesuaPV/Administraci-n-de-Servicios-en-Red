import sys
import rrdtool
import time

def fetch(agente):
    archivo = "RRDTools/"+agente.get('ip')+'_'+agente.get('comunidad')+".rrd"
    last_update = rrdtool.lastupdate(archivo)
    # Grafica desde la última lectura menos cinco minutos
    print(last_update)
    tiempo_inicial = int(last_update['date'].timestamp())- 60
    print(tiempo_inicial)
    rrdtool.dump(archivo, archivo.replace(".rrd", ".xml"))
    result = rrdtool.fetch(archivo, "-s,"+str(tiempo_inicial), "LAST")
    start, end, step = result[0]
    ds = result[1]
    rows = result[2]
    print(result)
    print(ds)
    print(rows)
