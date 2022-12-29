import telnetlib, socket


def createConfig():
    username = 'rcp'
    password = 'rcp'
    HOST = "30.30.30.1"
    tn = telnetlib.Telnet(HOST)

    tn.read_until(b"User: ")
    tn.write(username.encode('ascii') + b"\n")
    if password:
        tn.read_until(b"Password: ")
        tn.write(password.encode('ascii') + b"\n")
    tn.write(b"enable\n")
    tn.write(b"configure\n")
    tn.write(b"copy run start\n")
    tn.write(b"exit\n")
    tn.write(b"exit\n")

    print(tn.read_all().decode('ascii'))