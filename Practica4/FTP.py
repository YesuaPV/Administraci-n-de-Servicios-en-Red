from ftplib import FTP, all_errors


dir = "C:/Users/Yesua/OneDrive/Documents/ASR/Introduccion_SNMP/Practica4/Archivos/"

def iniciaFTP():

    ftp = FTP()
    HOST = input("Host destino: ")
    ftp.connect(HOST)
    ftp.login(input("Usuario: "), input("Password: "))
    print(ftp.getwelcome())
    op = 0
    while op == 0:
        cmd = input("cmd: ")
        comandos = cmd.split(" ")
        try:
            match comandos[0]:
                case "cd":
                    print(ftp.cwd(comandos[1]))
                case "rm":
                    if comandos[1].contains('.'):
                        ftp.delete(comandos[1])
                    else:
                        ftp.rmd(comandos[1])
                case "ls":
                    files = []
                    ftp.dir(files.append)
                    for f in files:
                        print(f)
                case "pwd":
                    print(ftp.pwd())
                case "mkd":
                    ftp.mkd(comandos[1])
                case "mv":
                    ftp.rename(comandos[1], comandos[2])
                case "put":
                    with open(dir+comandos[1], 'rb') as file:
                        ftp.storbinary('STOR '+comandos[2], file)
                case "get":
                    with open(dir+comandos[2], 'wb') as file:
                        ftp.retrbinary("RETR " + comandos[1], file.write)
                case "exit":
                    op = 1
                case default:
                    print("Comando invalido")
        except all_errors as e:
            print(f'\033[91m Error en FTP: {e} \033[0m')
    ftp.close()
