import os
import time

import pyautogui
from pysnmp.hlapi import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

from getSNMP import consultaSNMP
from ControladorBDD import leerAgentes
from ControladorBDD import eliminarAgente
from ControladorBDD import agregaAgente

from updateRRD import update
from graphRRD import grafica
from fetch import fetch
class bcolor:
  OK = '\033[92m'  # GREEN
  WARNING = '\033[93m'  # YELLOW
  FAIL = '\033[91m'  # RED
  RESET = '\033[0m'  # RESET COLOR



#MUESTRA AGENTES
def mostrarAgentes(opcion):
  print("\nLISTA DE AGENTES REGISTRADOS\n ")
  listaAgentes = leerAgentes()
  for idx, agente in enumerate(listaAgentes): #Muestra agentes del archivo
    print(str(idx+1) + ") " + agente.get("ip"))
    print("Comunidad: " + agente.get("comunidad"))
    print("Puerto: " + agente.get("puerto") + "\n")
    flag = 1
  if len(listaAgentes) == 0:
    print("No hay agentes registrados")
    return True
  while flag == 1:      #Solicita el agente para generar reporte
    print("Ingrese el indice del agente para realizar operacion: ")
    indice = input()
    flag = 0
    if int(indice) > len(listaAgentes) or int(indice) < 1:
      flag = 1
      print(bcolor.FAIL+"\n  *Indice incorrecto*"+bcolor.RESET)

  if int(opcion) == 1:
    update(agente)
  elif int(opcion) == 2:
    generarReporte(listaAgentes[int(indice)-1], indice)
  else:
    fetch(agente)

  return True


#GENERA REPORTE
def generarReporte(agente, id):
  #1667769660
  #1667769060
  print("\nTiempo inicial de la grafica (epoch)")
  iniTime = input()
  print("\nTiempo final de la grafica (epoch)")
  finTime = input()

  if not grafica(agente, iniTime, finTime):
    print("No se ha generado archivo rrd")
    return False

  print("\n\tGenerando reporte...")
  titulo = "reportes/"+agente.get('ip')+"-"+agente.get('comunidad')+"_"+str(datetime.now()).replace(' ', '_').replace(':', '_')+".pdf"
  canva = canvas.Canvas(titulo, pagesize=letter)
  canva.setLineWidth(.3)
  canva.setFont('Helvetica', 8)
  canva.drawString(25, 775, "Adminsitración de Servicios en Red - Práctica 2")
  canva.drawString(25, 760, "Pérez Vidales Yesua David - 4CM13")
  canva.setFont('Helvetica', 18)
  canva.drawString(225, 740, "Reporte agente " + str(datetime.now()).split(" ")[0])
  canva.setFont('Helvetica', 10)

  canva.drawString(50, 720, "version: 1")
  canva.drawString(50, 705, "device: " + consultaSNMP(agente, '1.3.6.1.2.1.1.5.0'))
  canva.drawString(50, 690, "description: " + consultaSNMP(agente, '1.3.6.1.2.1.1.1.0'))
  canva.drawString(50, 675, "date: " + str(datetime.now()))
  canva.drawString(50, 660, "defaultProtocol: radius")

  canva.drawString(50, 630, "rdate: " + str(datetime.now()))
  canva.drawString(50, 615, "#NAS-IP-Address")
  canva.drawString(50, 600, "4: " + agente.get('ip'))
  canva.drawString(50, 585, "#NAS-Port")
  canva.drawString(50, 570, "5: " + agente.get('puerto'))
  canva.drawString(50, 555, "#NAS-Port-Type")
  canva.drawString(50, 540, "5: 2")
  canva.drawString(50, 525, "#User-Name")
  canva.drawString(50, 510, "1: " + consultaSNMP(agente, '1.3.6.1.2.1.1.5.0'))
  canva.drawString(50, 495, "#Acct-Status-Type")
  canva.drawString(50, 480, "40: 2")
  canva.drawString(50, 465, "#Acct-Delay-Time")
  canva.drawString(50, 450, "41: 14")
  canva.drawString(50, 435, "#Acct-Input-Octets")
  canva.drawString(50, 420, "42: " + consultaSNMP(agente, '1.3.6.1.2.1.2.2.1.10.2'))
  canva.drawString(50, 405, "#Acct-Output-Octets")
  canva.drawString(50, 390, "43: " + consultaSNMP(agente, '1.3.6.1.2.1.2.2.1.16.2'))
  canva.drawString(50, 375, "#Acct-Session-Id")
  canva.drawString(50, 360, "44: " + id)
  canva.drawString(50, 345, "#Acct-Authentic")
  canva.drawString(50, 330, "45: 1")
  canva.drawString(50, 315, "#Acct-Session-Time")
  canva.drawString(50, 300, "46: " + consultaSNMP(agente, '1.3.6.1.2.1.1.3.0'))
  canva.drawString(50, 285, "#Acct-Input-Packets")
  inPackets = int(consultaSNMP(agente, '1.3.6.1.2.1.2.2.1.11.2')) + int(consultaSNMP(agente, '1.3.6.1.2.1.2.2.1.12.2'))
  canva.drawString(50, 270, "47: " + str(inPackets))
  canva.drawString(50, 255, "#Acct-Output-Packets")
  outPackets = int(consultaSNMP(agente, '1.3.6.1.2.1.2.2.1.17.2')) + int(consultaSNMP(agente, '1.3.6.1.2.1.2.2.1.18.2'))
  canva.drawString(50, 240, "48: " + str(outPackets))
  canva.drawString(50, 225, "#Acct-Terminate-Cause")
  canva.drawString(50, 210, "49: 11")
  canva.drawString(50, 195, "#Acct-Multi-Sesion-Id")
  canva.drawString(50, 180, "50: " + id)
  canva.drawString(50, 165, "#Acct-Link-Count")
  canva.drawString(50, 150, "51: 2")

  canva.showPage()

  canva.setFont('Helvetica', 8)
  canva.drawString(25, 775, "Adminsitración de Servicios en Red - Práctica 2")
  canva.drawString(25, 760, "Pérez Vidales Yesua David - 4CM13")
  canva.setFont('Helvetica', 18)
  canva.drawString(225, 740, "Reporte agente " + str(datetime.now()).split(" ")[0])
  canva.setFont('Helvetica', 10)

  widths = 280
  heights = 140
  canva.drawImage("images/ICMP.png", 20, 500, width=widths, height=heights)
  canva.drawImage("images/IPV4.png", 325, 500, width=widths, height=heights)
  canva.drawImage("images/TCP.png", 20, 300, width=widths, height=heights)
  canva.drawImage("images/UDP.png", 325, 300, width=widths, height=heights)
  canva.drawImage("images/Unicast.png", 20, 100, width=widths, height=heights)

  canva.drawString(200, 75, "Datos del " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(iniTime))))
  canva.drawString(220, 55, "al " + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(finTime))))

  canva.save()

  pyautogui.hotkey('ctrl', 'l')
  print(bcolor.OK + "\t-Reporte generado-" + bcolor.RESET)

  return ""




#MENU
flag = 0
flag2 = 1
while flag == 0 or flag2 == 0:
  flag2 = 1
  print(bcolor.OK+"\n\tSistema de Adminsitración de Red")
  print("\tPráctica 2: Administración de Contabilidad")
  print("\tPérez Vidales Yesua David \t4CM13\t2019630501"+bcolor.RESET)
  print("\n OPCIONES: ")
  print("1) Agregar agente\n2) Eliminar agente\n3) Administrar agente\notro) salir")
  op = input()
  if int(op) == 1:
    pyautogui.hotkey('ctrl', 'l')
    agregaAgente()
    pyautogui.hotkey('ctrl', 'l')
    print(bcolor.OK+"\t-Agente agregado-"+bcolor.RESET)
  elif int(op) == 2:
    pyautogui.hotkey('ctrl', 'l')
    borrados = eliminarAgente()
    pyautogui.hotkey('ctrl', 'l')
    print(bcolor.OK+"\t-Se eliminaron "+str(borrados)+" agentes-"+bcolor.RESET)
  elif int(op) == 3:
    pyautogui.hotkey('ctrl', 'l')
    print("OPCIONES: ")
    print("1) Monitorizar agente \n2) Generar reporte\n3) Generar XML\notro) regresar")
    op2 = input()
    if 0 < int(op2) < 4:
      if not mostrarAgentes(op2):
        print(bcolor.FAIL + "ERROR" + bcolor.RESET)
    else:
      pyautogui.hotkey('ctrl', 'l')
      flag2 = 0
  else:
    flag = 1
