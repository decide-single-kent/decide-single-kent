from django.urls import reverse
from .forms import AuthForm, QuestionForm, QuestionOptionFormSet, VotingForm
import django_filters.rest_framework
from django.conf import settings
from django.utils import timezone
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework import generics, status
from rest_framework.response import Response

from django.contrib.auth.decorators import login_required

from .models import Question, QuestionOption, Voting
from .serializers import SimpleVotingSerializer, VotingSerializer
from base.perms import UserIsStaff
from base.models import Auth
from django.utils.translation import gettext_lazy as _

class VotingView(generics.ListCreateAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    filterset_fields = ('id', )

    def get(self, request, *args, **kwargs):
        idpath = kwargs.get('voting_id')
        self.queryset = Voting.objects.all()
        version = request.version
        if version not in settings.ALLOWED_VERSIONS:
            version = settings.DEFAULT_VERSION
        if version == 'v2':
            self.serializer_class = SimpleVotingSerializer

        return super().get(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        self.permission_classes = (UserIsStaff,)
        self.check_permissions(request)
        for data in ['name', 'desc', 'question', 'question_opt']:
            if not data in request.data:
                return Response({}, status=status.HTTP_400_BAD_REQUEST)

        question = Question(desc=request.data.get('question'))
        question.save()
        for idx, q_opt in enumerate(request.data.get('question_opt')):
            opt = QuestionOption(question=question, option=q_opt, number=idx)
            opt.save()
        voting = Voting(name=request.data.get('name'), desc=request.data.get('desc'),
                question=question)
        voting.save()

        auth, _ = Auth.objects.get_or_create(url=settings.BASEURL,
                                          defaults={'me': True, 'name': 'test auth'})
        auth.save()
        voting.auths.add(auth)
        return Response({}, status=status.HTTP_201_CREATED)


class VotingUpdate(generics.RetrieveUpdateDestroyAPIView):
    queryset = Voting.objects.all()
    serializer_class = VotingSerializer
    filter_backends = (django_filters.rest_framework.DjangoFilterBackend,)
    permission_classes = (UserIsStaff,)

    def put(self, request, voting_id, *args, **kwars):
        action = request.data.get('action')
        if not action:
            return Response({}, status=status.HTTP_400_BAD_REQUEST)

        voting = get_object_or_404(Voting, pk=voting_id)
        msg = ''
        st = status.HTTP_200_OK
        if action == 'start':
            if voting.start_date:
                msg = 'Voting already started'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.start_date = timezone.now()
                voting.save()
                msg = 'Voting started'
        elif action == 'stop':
            if not voting.start_date:
                msg = 'Voting is not started'
                st = status.HTTP_400_BAD_REQUEST
            elif voting.end_date:
                msg = 'Voting already stopped'
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.end_date = timezone.now()
                voting.save()
                msg = _('Voting stopped')
        elif action == 'tally':
            if not voting.start_date:
                msg = _('Voting is not started')
                st = status.HTTP_400_BAD_REQUEST
            elif not voting.end_date:
                msg = _('Voting is not stopped')
                st = status.HTTP_400_BAD_REQUEST
            elif voting.tally:
                msg = _('Voting already tallied')
                st = status.HTTP_400_BAD_REQUEST
            else:
                voting.tally_votes(request.auth.key)
                msg = _('Voting tallied')
        else:
            msg = _('Action not found, try with start, stop or tally')
            st = status.HTTP_400_BAD_REQUEST
        return Response(msg, status=st)


@login_required(login_url='/no_autenticado')
def voting(request):
    if request.method == 'POST':
        form = VotingForm(request.POST)
        if form.is_valid():
            # Guarda la votación en la base de datos
            form.save()

            # Redirige a la página de detalles de la votación o a donde desees
            return redirect('/')
    else:
        form = VotingForm()

    return render(request, 'voting.html', {'form': form})


@login_required(login_url='/no_autenticado')
def question(request):
    if request.method == 'POST':
        form = QuestionForm(request.POST)
        formset = QuestionOptionFormSet(request.POST, instance=Question())

        if form.is_valid() and formset.is_valid():
            question_instance = form.save()
            formset.instance = question_instance
            formset.save()

            return redirect('close_windows/')  # o cualquier otra redirección que desees
    else:
        form = QuestionForm()
        formset = QuestionOptionFormSet(instance=Question())

    return render(request, 'new_question.html', {'form': form, 'formset': formset})

def close(request):
    return render(request, 'close_windows.html')

@login_required(login_url='/no_autenticado')
def auth(request):
    if request.method == 'POST':
        form = AuthForm(request.POST)
        if form.is_valid():
            form.save()

            return redirect(reverse('close_windows'))
    else:
        form = AuthForm()

    return render(request, 'new_auth.html', {'form': form})