import rrdtool

ret = rrdtool.create(
    "/home/linuxlite/PycharmProjects/Administraci-n-de-Servicios-en-Red/Practica3/ObtieneUmbrales/promedio.rrd",
    "--start", 'N',
    "--step", '15',
    "DS:CPUload:GAUGE:30:0:100",
    "DS:RAMload:GAUGE:30:0:100",
    "DS:InOctets:COUNTER:30:U:U",
    "DS:OutOctets:COUNTER:30:U:U",
    "RRA:AVERAGE:0.5:1:1000")
if ret:
    print(rrdtool.error())
