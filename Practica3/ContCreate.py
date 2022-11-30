import rrdtool
def ContcreateRRD(archivo):
    ret = rrdtool.create(
        "/home/linuxlite/PycharmProjects/Administraci-n-de-Servicios-en-Red/Practica3/"+archivo,
        "--start", 'N',
        "--step", '15',
        "DS:CPUload:GAUGE:60:0:100",
        "DS:RAMload:GAUGE:60:0:100",
        "DS:InOctets:COUNTER:60:U:U",
        "DS:OutOctets:COUNTER:60:U:U",
        "RRA:AVERAGE:0.5:1:2000")
    if ret:
        print(rrdtool.error())
