from Telnet import iniciaConexion
from FTP import iniciaFTP
import pyautogui

op = 1
while(op < 3 and op > 0):
  print('\033[92m' + "\n\tAdministración de configuracion")
  print("\tPráctica 4: Administración de Contabilidad")
  print("\tPérez Vidales Yesua David \t4CM13\t2019630501" + '\033[0m')

  print("\nMENU")
  print("\n1)Servicio TELNET\n2)Servicio FTP\notro)salir")
  op = int(input(": "))
  if op == 1:
      pyautogui.hotkey('ctrl', 'l')
      print('\033[92m' + "\tSERVICIO TELNET\n" +'\033[0m')
      iniciaConexion()
  elif op == 2:
      pyautogui.hotkey('ctrl', 'l')
      print('\033[92m' + "\tSERVICIO FTP\n" + '\033[0m')
      iniciaFTP()