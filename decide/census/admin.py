from django.contrib import admin
from email.message import EmailMessage
import smtplib
import ssl
from .models import Census
from voting.models import Voting
from django.contrib.auth.models import User
from django.conf import settings

class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id')
    list_filter = ('voting_id', )
    search_fields = ('voter_id', )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Datos para el envío de correo
        email = settings.EMAIL
        password = settings.PASSWORD

        # Datos del usuario
        user = User.objects.get(id=obj.voter_id)
        name_user = user.username
        email_envio = user.email

        # Verificar si el usuario tiene una dirección de correo electrónico antes de enviar el correo
        if email_envio:
            em = EmailMessage()
            em['Subject'] = 'Asignación de censo'
            em['From'] = email
            em['To'] = [email_envio]

            # Datos de la votación
            voting = Voting.objects.get(id=obj.voting_id)
            name_voting = voting.name
            desc_voting = voting.desc
            fecha_inicio = voting.start_date.date()

            # Contenido del correo
            text_content = (
                "Estimado usuario " + str(name_user) + ".\n\n" +
                "Se le ha asignado una nueva votación en la plataforma VotacionesM4. \n\n" +
                "Nombre: " + str(name_voting) + ".\n" +
                "Descripción: " + str(desc_voting) + ".\n" +
                "Fecha de inicio: " + str(fecha_inicio) + ".\n"
            )

            em.set_content(text_content)
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
                server.login(email, password)
                server.send_message(em)


admin.site.register(Census, CensusAdmin)