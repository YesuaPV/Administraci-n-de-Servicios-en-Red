import sys
import rrdtool
from Notify import send_alert_attached
import time
def detection(archivo, agente):
    rrdpath = '/home/linuxlite/PycharmProjects/Administraci-n-de-Servicios-en-Red/Practica3/'+archivo
    imgpath = '/home/linuxlite/PycharmProjects/Administraci-n-de-Servicios-en-Red/Practica3/images/'
    flagSobrepasa = 0


    ultima_lectura = int(time.time())
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 3600

    ret1 = rrdtool.graphv( imgpath+"ContCPU.png",
                         "--start", str(tiempo_inicial),
                         "--end", str(tiempo_final),
                        "--vertical-label=Cpu load",
                        '--lower-limit', '0',
                        '--upper-limit', '100',
                        "--title=Carga del CPU del agente Usando SNMP y RRDtools \n Detección de umbrales",
                        "DEF:cargaCPU="+rrdpath+":CPUload:AVERAGE",
                         "VDEF:cargaMAX=cargaCPU,MAXIMUM",
                         "VDEF:cargaMIN=cargaCPU,MINIMUM",
                         "VDEF:cargaSTDEV=cargaCPU,STDEV",
                         "VDEF:cargaLAST=cargaCPU,LAST",
                         "CDEF:umbral85=cargaCPU,85,LT,0,cargaCPU,IF",
                         "AREA:cargaCPU#00FF00:Carga del CPU",
                         "AREA:umbral85#FF9F00:Carga CPU mayor que 85",
                         "HRULE:85#FF0000:Umbral 85%",
                         "PRINT:cargaLAST:%6.2lf",
                         "GPRINT:cargaMIN:%6.2lf %SMIN",
                         "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                         "GPRINT:cargaLAST:%6.2lf %SLAST")
    ret2 = rrdtool.graphv(imgpath + "ContRAM.png",
                          "--start", str(tiempo_inicial),
                          "--end", str(tiempo_final),
                          "--vertical-label=RAM load",
                          '--lower-limit', '0',
                          '--upper-limit', '100',
                          "--title=Carga de RAM del agente Usando SNMP y RRDtools \n Detección de umbrales",
                          "DEF:cargaRAM=" + rrdpath + ":RAMload:AVERAGE",
                          "VDEF:cargaMAX=cargaRAM,MAXIMUM",
                          "VDEF:cargaMIN=cargaRAM,MINIMUM",
                          "VDEF:cargaSTDEV=cargaRAM,STDEV",
                          "VDEF:cargaLAST=cargaRAM,LAST",
                          "CDEF:umbral60=cargaRAM,60,LT,0,cargaRAM,IF",
                          "CDEF:umbral70=cargaRAM,70,LT,0,cargaRAM,IF",
                          "CDEF:umbral80=cargaRAM,80,LT,0,cargaRAM,IF",
                          "AREA:cargaRAM#00FF00:Carga de RAM",
                          "AREA:umbral60#FFFF00:Carga RAM mayor que 60",
                          "AREA:umbral70#BB9F00:Carga RAM mayor que 70",
                          "AREA:umbral80#FF2200:Carga RAM mayor que 80",
                          "HRULE:80#FF0000:Umbral 80%",
                          "HRULE:70#FF0000:Umbral 70%",
                          "HRULE:60#FF0000:Umbral 60%",
                          "PRINT:cargaLAST:%6.2lf",
                          "GPRINT:cargaMIN:%6.2lf %SMIN",
                          "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                          "GPRINT:cargaLAST:%6.2lf %SLAST")
    ret3 = rrdtool.graphv(imgpath + "ContRED.png",
                          "--start", str(tiempo_inicial),
                          "--end", str(tiempo_final),
                          "--vertical-label=RED load",
                          '--lower-limit', '0',
                          '--upper-limit', '100',
                          "--title=Uso de RED del agente Usando SNMP y RRDtools \n Detección de umbrales",
                          "DEF:cargaRED=" + rrdpath + ":InOctets:AVERAGE",
                          "DEF:cargaREDout=" + rrdpath + ":OutOctets:AVERAGE",
                          "VDEF:cargaLAST=cargaRED,LAST",
                          "CDEF:umbral2k=cargaRED,2000,LT,0,cargaRED,IF",
                          "AREA:cargaRED#00FF00:Uso de RED",
                          "AREA:umbral2k#FF9F00:Uso de RED mayor que 2kb",
                          "HRULE:2000#FF0000:Umbral 2kb",
                          "PRINT:cargaLAST:%6.2lf",
                          "GPRINT:cargaLAST:%6.2lf %SLAST")

    ultimo_valorCPU = float(ret1['print[0]'])
    ultimo_valorRAM = float(ret2['print[0]'])
    ultimo_valorRED = float(ret3['print[0]'])
    print("VALORES OBTENIDOS : " + ret1['print[0]'] + ret2['print[0]'] + ret3['print[0]'])
    umbral = {
        "go": 0,
        "set": 0,
        "ready": 0
    }

    #if ultimo_valorCPU > 80:
     #   subject = subject + "CPU "
      #  print("Sobrepasa Umbral CPU línea base")
       # umbral["cpu"] = 1
        #flagSobrepasa = 1

    if ultimo_valorRAM > 80:
        subject = "Sobrepasa el umbral: RAM"
        print("Sobrepasa Umbral RAM línea base")
        flagSobrepasa = 1
        umbral["go"] = 1
    elif ultimo_valorRAM > 70:
        subject = "Condicion Set: RAM"
        print("Sobrepasa set RAM línea base")
        flagSobrepasa = 1
        umbral["set"] = 1
    elif ultimo_valorRAM > 60:
        subject = "Condicion Ready: RAM"
        print("Sobrepasa ready RAM línea base")
        flagSobrepasa = 1
        umbral["ready"] = 1
    #if ultimo_valorRED > 2000:
     #   subject = subject + "RED "
      #  print("Sobrepasa Umbral RED línea base")
       # flagSobrepasa = 1
        #umbral["red"] = 1

    if flagSobrepasa == 1:
        send_alert_attached(subject, umbral, agente)
