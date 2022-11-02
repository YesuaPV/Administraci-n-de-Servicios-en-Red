import os

import pyautogui
from pysnmp.hlapi import *
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from datetime import datetime

from ControladorBDD import leerAgentes
from ControladorBDD import eliminarAgente
from ControladorBDD import agregaAgente


class bcolor:
  OK = '\033[92m'  # GREEN
  WARNING = '\033[93m'  # YELLOW
  FAIL = '\033[91m'  # RED
  RESET = '\033[0m'  # RESET COLOR



#MUESTRA AGENTES
def mostrarAgentes():
  print("\nLISTA DE AGENTES REGISTRADOS\n ")
  listaAgentes = leerAgentes()
  for idx, agente in enumerate(listaAgentes): #Muestra agentes del archivo
    print(str(idx+1) + ") " + agente.get("ip"))
    print("Comunidad: " + agente.get("comunidad"))
    print("Puerto: " + agente.get("puerto") + "\n")
    flag = 1
  if(len(listaAgentes) == 0):
    print("No hay agentes registrados")
    return False
  while flag == 1:      #Solicita el agente para generar reporte
    print("Ingrese el indice del agente para generar reporte: ")
    indice = input()
    flag = 0
    if int(indice) > len(listaAgentes) or int(indice) < 1:
      flag = 1
      print(bcolor.FAIL+"\n  *Indice incorrecto*"+bcolor.RESET)

  obtenerDatosAgente(listaAgentes[int(indice)-1])
  return True


#GENERA REPORTE
def obtenerDatosAgente(agente):
  nombreArchivo = agente.get('ip').replace(".", "-") + "_" + agente.get('comunidad') + ".rrd"


  print("\n\tGenerando reporte...")
  titulo = "reportes/"+agente.get('ip')+"-"+agente.get('comunidad')+"_"+str(datetime.now()).replace(' ', '_').replace(':', '_')+".pdf"
  canva = canvas.Canvas(titulo, pagesize=letter)
  canva.setLineWidth(.3)
  canva.setFont('Helvetica', 8)
  canva.drawString(25, 775, "Adminsitración de Servicios en Red - Práctica 1")
  canva.drawString(25, 760, "Pérez Vidales Yesua David - 4CM13")
  canva.setFont('Helvetica', 14)
  canva.drawString(225, 740, "Reporte agente " + str(datetime.now()).split(" ")[0])
  canva.setFont('Helvetica', 8)

  canva.save()

  return ""




#MENU
flag = 0
while flag == 0:
  print(bcolor.OK+"\n\tSistema de Adminsitración de Red")
  print("\tPráctica 2: Administración de Contabilidad")
  print("\tPérez Vidales Yesua David \t4CM13\t2019630501"+bcolor.RESET)
  print("\n OPCIONES: ")
  print("1) Agregar agente\n2) Eliminar agente\n3) Administrar agente\notro) salir")
  op = input()
  if int(op) == 1:
    pyautogui.hotkey('ctrl', 'l')
    agregaAgente()
    pyautogui.hotkey('', 'l')
    print(bcolor.OK+"\t-Agente agregado-"+bcolor.RESET)
  elif int(op) == 2:
    pyautogui.hotkey('ctrl', 'l')
    borrados = eliminarAgente()
    pyautogui.hotkey('ctrl', 'l')
    print(bcolor.OK+"\t-Se eliminaron "+str(borrados)+" agentes-"+bcolor.RESET)
  elif int(op) == 3:
    pyautogui.hotkey('ctrl', 'l')
    if mostrarAgentes():
      pyautogui.hotkey('ctrl', 'l')
      print(bcolor.OK+"\t-Reporte generado-"+bcolor.RESET)
  else:
    flag = 1
