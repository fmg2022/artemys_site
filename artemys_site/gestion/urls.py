# from django.contrib.auth.views import LogoutView
from django.urls import path
from django.contrib.auth.views import PasswordResetCompleteView, PasswordResetConfirmView, PasswordResetDoneView, PasswordResetView

from . import views

urlpatterns = [
  # Página principal
  path("", views.index, name="index"),

  # Información de la empresa
  path("info/", views.info, name="info"),
  path("politicas_de_garantia/", views.garantia_policy, name="garantia_policy"),
  path("politicas_de_turnos/", views.turnos_policy, name="turnos_policy"),

  # Servicios
  path("servicios/",views.TipoServiciosView.as_view(), name="servicios"),
  path("servicios/lista/", views.getAllServices, name="lista_servicios"),
	
  # Acceso denegado
	path("solicitud_denegada/", views.soli_deneg, name="denegado"),

  # Usuarios
	path("registro/", views.register, name="registro"),
	path("login/", views.login_view, name="login"),
	path("logout/", views.my_logout, name="logout"),
	path("usuario/<int:pk>/", views.user_detail, name="usuario"),

  # Contraseñas
  	path("reset/passwordReset/", PasswordResetView.as_view(template_name="panels/passwordReset/psw_reset_form.html"), name="PasswordReset"),
    path("reset/done/",PasswordResetDoneView.as_view(template_name ="panels/passwordReset/psw_reset_done.html"), name="password_reset_done"),
    path("reset/PasswordResetConfirm/<uidb64>/<token>/", PasswordResetConfirmView.as_view(template_name ="panels/passwordReset\psw_reset_confirm.html"), name="PasswordResetConfirm"),
    path("reset/complete/", PasswordResetCompleteView.as_view(template_name = "panels/passwordReset/psw_reset_complete.html"), name= "password_reset_complete"),

  # Turnos
    path("turno/", views.setNewTurn, name="turno"),
    path("turnos/", views.getMyTurns, name="turnos"),
    path("turno/cancelar/<int:pk>", views.deleteTurn, name="turno_cancelar"),
]
