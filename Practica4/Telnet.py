import telnetlib, socket

def iniciaConexion():

    HOST = input("Host destino: ")
    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"User: ")
    username = input("User: ")
    tn.write(username.encode('ascii') + b"\n")
    password = input("Password: ")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
    tn.write(b"enable\n")
    tn.write(b"configure\n")
    op = 1
    while (op < 3 and op > 0):
        op = int(input("Selecciones su opción \n1)Crear archivo startup.conf \n2)Activar servicio FTP \notro)salir\n"))
        match op:
            case 1:
                tn.write(b"copy run start\n")
                tn.write(b"exit\n")
                tn.write(b"exit\n")
                print(tn.read_all().decode('ascii'))
                op = 5
            case 2:
                tn.write(b"service ftp\n")
                tn.write(b"exit\n")
                tn.write(b"exit\n")
                print(tn.read_all().decode('ascii'))
                op = 5
            case default:
                tn.write(b"exit\n")
                tn.write(b"exit\n")
                print(tn.read_all().decode('ascii'))
                tn.close()
                return