import os

#ELIMINAR AGENTES
def eliminarAgente():
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
  return borrados


#LEER LISTA DE AGENTES
def leerAgentes():
  listaAgentes = []
  with file_open("agentes.txt", "r") as archivo:
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


#ANADIR AGENTES
def agregaAgente():
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
  return True


#ABRIR ARCHIVOS
def file_open(name, mode):
  try:
    file = open(name, mode)
    return file
  except OSError as err:
    print("Error: {0}".format(err))
  return