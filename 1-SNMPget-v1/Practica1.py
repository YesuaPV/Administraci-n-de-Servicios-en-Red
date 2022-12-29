import os

import pyautogui
from pysnmp.hlapi import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

class bcolor:
  OK = '\033[92m'  # GREEN
  WARNING = '\033[93m'  # YELLOW
  FAIL = '\033[91m'  # RED
  RESET = '\033[0m'  # RESET COLOR

def file_open(name, mode): #Abrir archivos
  try:
    file = open(name, mode)
    return file
  except OSError as err:
    print("Error: {0}".format(err))
  return


def agregaAgente(): #Agregar un agente SNMP
  print("\n\n\t ***** AÑADIENDO AGENTE SNMP *****\n")
  print("Agregue la direccion ip: ")
  ip = input()
  print("Agregue el nombre de la comunidad: ")
  comunidad = input()
  print("Agregue el puerto del agente: ")
  puerto = input()
  print("Agregue la version de la MIB: ")
  version = input()

  archivo = file_open("agentes.txt", "a")
  archivo.write(ip + "," + comunidad + "," + puerto + "," + version + "\n")
  archivo.close()
  print("\n  Agente Creado")


def eliminarAgente(): #Eliminar un agente SNMP
  print("\n\n\t ***** ELIMINANDO AGENTE SNMP *****\n")
  print("Dirección IP del agenete: ")
  ip = input()
  print("Comunidad del agente: ")
  comunidad = input()
  borrados = 0
  with open("agentes.txt", "r") as lectura:
    with open("agentesTemp.txt", "w") as salida:
      for line in lectura:
        datos = line.split(",")
        if datos[0] == ip and datos[1] == comunidad:
          borrados = borrados + 1
        else:
          salida.write(line)
  os.replace('agentesTemp.txt', 'agentes.txt')
  lectura.close()

  dir = 'reportes/'
  for f in os.listdir(dir):
    if((ip in f) and (comunidad in f)):
      os.remove(os.path.join(dir, f))
  return borrados


def consultaSNMP(agente,OID):
  ip = agente.get("ip")
  nombreComunidad = agente.get("comunidad")
  puerto = str(agente.get("puerto"))

  iterator = getCmd(
    SnmpEngine(),
    CommunityData(nombreComunidad, mpModel=0),
    UdpTransportTarget((ip, puerto)),
    ContextData(),
    ObjectType(ObjectIdentity(OID))
  )
  errorIndication, errorStatus, errorIndex, varBinds = next(iterator)
  if errorIndication:
    print(errorIndication)

  elif errorStatus:
    print('%s at %s' % (errorStatus.prettyPrint(),
    errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))

  else:
    texto = ""
    for varBind in varBinds:
      texto = texto + (' = '.join([x.prettyPrint() for x in varBind]))
    return texto


def obtenerDatosAgente(agente):
  OIDs = {
    'SO': '1.3.6.1.2.1.1.1.0',
    'Nombre': '1.3.6.1.2.1.1.5.0',
    'Ubicacion': '1.3.6.1.2.1.1.6.0',
    'numeroInterfaces': '1.3.6.1.2.1.2.1.0',
    'nombreInterface': '1.3.6.1.2.1.2.2.1.2.',
    'statusInterface': '1.3.6.1.2.1.2.2.1.8.',
    'tiempoActividad': '1.3.6.1.2.1.1.3.0'
  }

  print("\n\tGenerando reporte...")
  titulo = "reportes/"+agente.get('ip')+"-"+agente.get('comunidad')+"_"+str(datetime.now()).replace(' ','_').replace(':','_')+".pdf"
  canva = canvas.Canvas(titulo,pagesize=letter)
  canva.setLineWidth(.3)
  canva.setFont('Helvetica', 8)
  canva.drawString(25, 775, "Adminsitración de Servicios en Red - Práctica 1")
  canva.drawString(25, 760, "Pérez Vidales Yesua David - 4CM13")
  canva.setFont('Helvetica', 14)
  canva.drawString(225, 740, "Reporte agente " + str(datetime.now()).split(" ")[0])
  canva.setFont('Helvetica', 8)
  canva.drawString(25, 740,str(datetime.now()).split(" ")[1].split(".")[0])
  canva.setFont('Helvetica', 12)
  canva.drawString(50,690,"IP : " + agente.get('ip'))
  canva.drawString(300,690,"Puerto: " + agente.get('puerto'))
  canva.drawString(50,670,"Comunidad: " + agente.get('comunidad'))
  canva.drawString(300, 6700, "MIB: v" + agente.get('version'))
  canva.drawString(50,650,"Host: " + str(consultaSNMP(agente,OIDs.get('Nombre'))).split("= ")[1])
  so1 = consultaSNMP(agente,OIDs.get('SO'))
  if so1.find("Windows") != -1:
    canva.drawImage("logo/win.jpg",400,570, width=200, height=200)
    so = consultaSNMP(agente, OIDs.get('SO')).split("Software: ")[1].split("(")[0]
  elif so1.find("Linux") != -1:
    canva.drawImage("logo/linux.jpg",400,600, width=200, height=130)
    so = consultaSNMP(agente, OIDs.get('SO')).split(" ")[5]
  else:
    canva.drawImage("logo/otro.jpg",400,570, width=200, height=200)
    so = consultaSNMP(agente, OIDs.get('SO')).split("= ")[1]
  canva.drawString(445,600, so )
  canva.drawString(50,630,"Ubicación: " + consultaSNMP(agente,OIDs.get('Ubicacion')).split("= ")[1])
  canva.drawString(50,610,"Tiempo de actividad: " + str(int(consultaSNMP(agente, OIDs.get('tiempoActividad')).split("= ")[1])/100) + "s")
  interfaces = int(consultaSNMP(agente,OIDs.get('numeroInterfaces')).split("= ")[1])
  canva.drawString(250,580,"  Numero de interfaces: " + str(interfaces))
  canva.line(25, 570, 600, 570)
  canva.setFont('Helvetica', 11)
  canva.drawString(30,550,"Nombre de la Interface")
  canva.drawString(500, 550, "Status")
  linea = 550
  if interfaces > 15:
    interfaces = 15
  for i in range (interfaces):
    linea = linea - 15
    if linea < 30:
      canva.showPage()
      canva.setFont('Helvetica', 11)
      canva.drawString(30, 715, "Nombre de la Interface")
      canva.drawString(500, 715, "Status")
      linea = 700
    canva.setFont('Helvetica', 9)
    if so1.find("VirtualBox") != -1:
      nombre = str(consultaSNMP(agente, OIDs.get('nombreInterface') + str(i + 1))).split("= ")[1]
      canva.drawString(35, linea, nombre)
    else:
      var = str(consultaSNMP(agente, OIDs.get('nombreInterface') + str(i + 1)))
      splited = var[var.index('x') + 1:len(var)]
      nombre = bytes.fromhex(splited).decode('utf-8')
      canva.drawString(35, linea, nombre[0:len(nombre) - 1])

    status = consultaSNMP(agente,OIDs.get('statusInterface')+str(i+1)).split("= ")[1]
    canva.drawString(500, linea, status)
    #if int(status) == 1:

    #elif int(status) == 2:
    #  canva.drawString(500, linea, "down")
    #else:
    #  canva.drawString(500, linea, "testing")
  canva.save()

  return ""

def leerAgentes():
  listaAgentes = []
  with file_open("agentes.txt","r") as archivo:
    for agentes in archivo :
      datos = agentes.split(",")
      agente = {
        "ip" : datos[0],
        "comunidad" : datos[1],
        "puerto" : datos[2],
        "version" : datos[3].strip('\n')
      }
      listaAgentes.append(agente)
  return listaAgentes

def mostrarAgentes():
  print("\nLISTA DE AGENTES REGISTRADOS\n ")
  listaAgentes = leerAgentes()
  for idx, agente in enumerate(listaAgentes): #Muestra agentes del archivo
    print(str(idx+1) + ") " + agente.get("ip"))
    print("Comunidad: " + agente.get("comunidad"))
    print("Puerto: " + agente.get("puerto") + "\n")

  flag = 1
  while flag == 1:      #Solicita el agente para generar reporte
    print("Ingrese el indice del agente para generar reporte: ")
    indice = input()
    flag = 0
    if int(indice) > len(listaAgentes) or int(indice) < 1:
      flag = 1
      print(bcolor.FAIL+"\n  *Indice incorrecto*"+bcolor.RESET)
  obtenerDatosAgente(listaAgentes[int(indice)-1])


#MENU
flag = 0
while flag == 0:
  print(bcolor.OK+"\n\tSistema de Adminsitración de Red")
  print("\tPráctica 1: Administración de Información")
  print("\tPérez Vidales Yesua David \t4CM13\t2019630501"+bcolor.RESET)
  print("\n OPCIONES: ")
  print("1) Agregar agente\n2) Eliminar agente\n3) Hacer reporte de un agente\notro) salir")
  op = input()
  if int(op) == 1:
    pyautogui.hotkey('ctrl','l')
    agregaAgente()
    pyautogui.hotkey('ctrl','l')
    print(bcolor.OK+"\t-Agente agregado-"+bcolor.RESET)
  elif int(op) == 2:
    pyautogui.hotkey('ctrl','l')
    borrados = eliminarAgente()
    pyautogui.hotkey('ctrl','l')
    print(bcolor.OK+"\t-Se eliminaron "+str(borrados)+" agentes-"+bcolor.RESET)
  elif int(op) == 3:
    pyautogui.hotkey('ctrl','l')
    mostrarAgentes()
    pyautogui.hotkey('ctrl','l')
    print(bcolor.OK+"\t-Reporte generado-"+bcolor.RESET)
  else:
    flag = 1
