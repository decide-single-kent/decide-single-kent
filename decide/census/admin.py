from django.contrib import admin
from email.message import EmailMessage
import smtplib
import ssl
from .models import Census
from voting.models import Voting
from django.contrib.auth.models import User

class CensusAdmin(admin.ModelAdmin):
    list_display = ('voting_id', 'voter_id')
    list_filter = ('voting_id', )
    search_fields = ('voter_id', )

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)
        email_envio = User.objects.get(id=obj.voter_id).email
        correo = "ronmonalb@gmail.com"
        password = "zndnmdhugwcrwatt"
        #email_envio = "ronaldmontoya2002@gmail.com"

        em = EmailMessage()
        em['Subject'] = 'Asignación de censo'
        em['From'] = correo
        em['To'] = [email_envio]

        # Ensure that the census is a string
        voting = Voting.objects.get(id=obj.voting_id).name
        desc_voting = Voting.objects.get(id=obj.voting_id).desc
        fecha_inicio = Voting.objects.get(id=obj.voting_id).start_date.date()
        text_content = (
            "Se le ha asignado una nueva votación en la plataforma VotacionesM4.\n\n" +
            "Nombre: "+ str(voting) + "\n" +
            "Descripción: " + str(desc_voting) + "\n" +
            "Fecha de inicio: " + str(fecha_inicio) + "\n"
        )

        em.set_content(text_content)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(correo, password)

            # Use the send method instead of item assignment
            server.send_message(em)

# Register the Census model with the customized admin
admin.site.register(Census, CensusAdmin)
