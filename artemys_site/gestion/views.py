from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.http import Http404
from django.views.generic import ListView
from django.shortcuts import redirect, render

from gestion.models import ServiceType, Profile
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


# # def principal(request):
# #     comentarios = Comentario.objects.all()
# #     tt = TipoTrabajo.objects.all()
# #     return render(request, 'pagprincipal.html', {'comentarios':comentarios, 'tipoTrabajos':tt})

# # def turnos_calendar(request):
# #     turnos = Turno.objects.all()
# #     return render(request, 'turno_list.html', {'turnos': turnos, 'form': TurnoForm(request.user.id)})


# ------------------------------- Tipos de servicios --------------------------------
class TipoServiciosView(ListView):
  model = ServiceType
  context_object_name = 'servicios'
  template_name = "panels/servicios/servicios.html"

# ------------------------------- Turnos --------------------------------
# def turn(request):
#   form = TurnForm()
#   return render(request, "form.html", {'form': form})

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
      return redirect('inicio')
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
