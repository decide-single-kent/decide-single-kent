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
        # Call the save_model method of the base class to perform the standard saving
        super().save_model(request, obj, form, change)
        usuario = User.objects.get(id=obj.voter_id).username
        email_envio = User.objects.get(id=obj.voter_id).email
        # Add your logic here, for example, sending an email after saving the object
        correo = "ronmonalb@gmail.com"
        password = "zndnmdhugwcrwatt"
        #email_envio = "ronaldmontoya2002@gmail.com"

        em = EmailMessage()
        em['Subject'] = 'Asignación de censo'
        em['From'] = correo
        em['To'] = [email_envio]

        # Ensure that the census is a string
        voting = Voting.objects.get(id=obj.voting_id).name
        em.set_content('Se le ha asignado el censo para votar en la plataforma VotacionesM4 , La votación se llama: ' + str(voting) + ' y su usuario es: ' + str(usuario))

        context = ssl.create_default_context()
        with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as server:
            server.login(correo, password)

            # Use the send method instead of item assignment
            server.send_message(em)

# Register the Census model with the customized admin
admin.site.register(Census, CensusAdmin)
