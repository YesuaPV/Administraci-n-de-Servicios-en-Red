import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from getSNMP import consultaSNMP
import time

COMMASPACE = ', '
# Define params
imgpath = '/home/linuxlite/PycharmProjects/Administraci-n-de-Servicios-en-Red/Practica3/images/'
fname = 'trend.rrd'

mailsender = "dummycuenta3@gmail.com"
mailreceip = "yesuaperez1@gmail.com"
mailserver = 'smtp.gmail.com: 587'
password = 'dvduuffmlhspbmjj'


def send_alert_attached(subject, umbral, agente):
    """ Envía un correo electrónico adjuntando la imagen en IMG
    """
    body = '<table style="width:80%; border: 2px solid black;  border-collapse: collapse">' \
           '<tr style="height:35px">' \
           '<th style="border: 1px solid black">Nombre del dispositivo</th>' \
           '<th style="border: 1px solid black">Version del software</th>' \
           '<th style="border: 1px solid black">Tiempo de actividad</th>' \
           '<th style="border: 1px solid black">Fecha y hora del host</th>' \
           '<th style="border: 1px solid black">Comunidad SNMP</th>' \
           '</tr>' \
           '<tr style="height:50px">' \
           '<td style="padding: 5px">' + consultaSNMP(agente, "1.3.6.1.2.1.1.5.0") + '</td>' \
           '<td style="padding: 5px">' + consultaSNMP(agente, "1.3.6.1.2.1.1.1.0") + '</td>' \
           '<td style="padding: 5px">' + consultaSNMP(agente, "1.3.6.1.2.1.1.3.0") + '</td>' \
           '<td style="padding: 5px">' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(int(time.time()))) + '</td>' \
           '<td style="padding: 5px">' + agente.get("comunidad") + '</td>' \
           '</tr>' \
           '</table>'

    msg = MIMEMultipart()
    msg['Subject'] = subject
    msg['From'] = mailsender
    msg['To'] = mailreceip
    msg.attach(MIMEText(body, 'html'))
    #if umbral.get("cpu") == 1:
        #fp = open(imgpath + 'ContCPU.png', 'rb')
        #img = MIMEImage(fp.read())
        #fp.close()
        #msg.attach(img)
    #if umbral.get("ram") == 1:
    fp = open(imgpath + 'ContRAM.png', 'rb')
    img = MIMEImage(fp.read())
    fp.close()
    msg.attach(img)
    #/if umbral.get("red") == 1:
       # fp = open(imgpath + 'ContRED.png', 'rb')
       # img = MIMEImage(fp.read())
       # fp.close()
      #  msg.attach(img)
    s = smtplib.SMTP(mailserver)

    s.starttls()
    # Login Credentials for sending the mail
    s.login(mailsender, password)

    s.sendmail(mailsender, mailreceip, msg.as_string())
    s.quit()
