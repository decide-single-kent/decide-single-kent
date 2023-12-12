from django.contrib.auth.views import LoginView
from django.views.generic.edit import CreateView
from django.shortcuts import render, redirect
from django.contrib.auth import logout
from census.models import Census
from voting.models import Voting
from django.utils import timezone
from django.contrib.auth.decorators import login_required

from .forms import SignUpForm 

def home(request):
  return render(request, 'core/index.html', {"usuario": request.user})

def signup(request):
  if request.method == 'POST':
    form = SignUpForm(request.POST)

    if form.is_valid():
      form.save()
      return redirect('/login/' )
  else:
    form = SignUpForm()

  return render(request, 'core/signup.html', {
    'form': form
  })
def logout_view(request):
  logout(request)
  return redirect('/')


@login_required(login_url='/no_autenticado')
def assigned_census(request):
    current_datetime = timezone.now()

    # Filtrar los censos asignados
    census = Census.objects.filter(voter_id=request.user.id)

    # Filtrar las votaciones que tienen fecha de inicio pero no de finalización
    votings = []
    for c in census:
        vot = Voting.objects.filter(id=c.voting_id, start_date__isnull=False, end_date__isnull=True, start_date__lte=current_datetime).first()
        if vot:
            votings.append(vot)

    return render(request, 'core/assigned_census.html', {"census": census, "votings": votings})
