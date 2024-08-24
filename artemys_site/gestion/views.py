from django.core.exceptions import ObjectDoesNotExist
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import Http404, JsonResponse
from django.views.generic import ListView
from django.shortcuts import redirect, render

from datetime import datetime, timedelta

from gestion.models import ServiceType, Profile, Turn
from gestion.forms import CustomUserForm, ProfileForm, TurnForm


def index (request):
  return render(request, 'index.html')

# ----------------------------------- Generales ------------------------------------
def info(request):
  return render(request, 'panels/info/infoUs.html')

def turnos_policy(request):
  return render(request, 'panels/info/turnosPolicy.html')

def garantia_policy(request):
  return render(request, 'panels/info/garantiaPolicy.html')

def soli_deneg (request):
  return render(request, '_partials/requestDenied.html')

# ------------------------------- Tipos de servicios --------------------------------
class TipoServiciosView(ListView):
  model = ServiceType
  context_object_name = 'servicios'
  template_name = "panels/servicios/servicios.html"

def getAllServices(request):
  data = list(ServiceType.objects.values('id', 'serName'))
  return JsonResponse({'data': data})

# Función que devuelva un json con los datos de todos los servicios (de momento, después será con un límite [n] -> para hacerlo paginado)
# https://stackoverflow.com/questions/67723387/fetch-data-from-django-backend-having-parts-of-dynamic-url-private

# ------------------------------- Turnos --------------------------------
def setNewTurn(request):
  profile = Profile.objects.get(user__id=request.user.id)
  if request.method == 'POST':
    form = TurnForm(request.POST)
    if form.is_valid():
      turn = form.save(commit=False)
      turn.turDate = form.cleaned_data['turDate']
      turn.turHrFrom = form.cleaned_data['turHrFrom']
      # obtener del 'serviceType' el tiempo 'serTime', de ahí sumarlos
      # https://stackoverflow.com/questions/2780897/python-summing-up-time
      # validar si el tiempo establecido
      turn.serviceType = form.cleaned_data['serviceType']
      turn.profile = profile
      turn.save()
      return redirect('index')
  else:
    form = TurnForm()
  return render(request, "panels/turnos/turn.html", {'form': form})

def deleteTurn(request, pk):
  try:
    turn = Turn.objects.get(pk=pk)
    turn.isActive = False
    turn.save()
    messages.success(request, 'El turno ha sido cancelado')
  except:
    messages.error(request, 'No es posible cancelar el turno')

  return redirect('index')

def getMyTurns(request):
  try:
    profile = Profile.objects.values('id').get(user__id=request.user.id)
    results = list(Turn.objects.values('id', 'serviceType__serName', 'turDate', 'turHrFrom', 'serviceType__serTime').filter(profile_id=profile['id']).filter(isActive=True))
    turns = []
    for fila in results:
      startDate = datetime.combine(fila['turDate'], fila['turHrFrom'])
      time = fila['serviceType__serTime']
      endDate = startDate +  timedelta(hours=time.hour, minutes=time.minute, seconds=time.second)
      el = {'id': fila['id'], 'title': fila['serviceType__serName'], 'start': startDate, 'end': endDate}
      turns.append(el)
  except ObjectDoesNotExist:
    turns = {'401': 'Sin autorización'}
  return JsonResponse(turns, safe=False)

# ----------------------------------- Perfiles -------------------------------------
def register(request):
  if request.method == "POST":
    formularios = [CustomUserForm(request.POST), ProfileForm(request.POST)]
    is_valid = formularios[0].is_valid() and formularios[1].is_valid()
    if is_valid:
      user = formularios[0].save()
      profile = formularios[1].save(commit=False)
      profile.user = user
      profile.save()

      login(request, user)
      messages.success(request, f'Usuario {user} ha sido creado')
      return redirect('index')
  else:
    formularios = [CustomUserForm(), ProfileForm()]
  return render(request, 'panels/perfiles/register.html', {'forms': formularios})

def user_detail(request, pk):
  try:
    perfil = Profile.objects.get(pk=pk)
  except Profile.DoesNotExist:
    raise Http404("El perfil no existe")
  return render(request, "panels/perfiles/profile.html", {'perfil': perfil})

def login_view(request):
  if request.method == "POST":
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(request, username=username, password=password)
    if user is not None:
      login(request, user)
      messages.success(request, "Has iniciado sesión")
      return redirect('index')
    else:
      messages.info(request, "Usuario o Contraseña incorrecto, intente nuecamente.")
  return render(request, "panels/perfiles/login.html")

def my_logout(request):
  logout(request)
  messages.info(request, "Te has desconectado")
  return redirect('index')
