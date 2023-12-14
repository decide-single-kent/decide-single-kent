from django.db.utils import IntegrityError
from django.core.exceptions import ObjectDoesNotExist

from email.message import EmailMessage
import ssl
import smtplib

def enviar_correo_asignación_censo():
        correo = "ronmonalb@gmail.com"
        password = "zndnmdhugwcrwatt"
        email_envio = "ronaldmontoya2002@gmail.com"

        em = EmailMessage()
        em['Subject'] = 'Asignación de censo'
        em['From'] = correo
        em['To'] = email_envio

        # Asegúrate de que censo sea una cadena
        em.set_content('Se le ha asignado el censo  para votar en la plataforma Decide')

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(correo, password)
                
                # Utiliza el método send en lugar de sendmail y send_message
                server.send_message(em)