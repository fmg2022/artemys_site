from django.forms import ModelForm, DateInput, NumberInput, TextInput, Textarea, TimeInput
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

from gestion.models import Profile, Turn

import re
from datetime import date

class ProfileForm(ModelForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'input-control'

  class Meta:
    model = Profile
    fields = ("__all__")
    # https://stackoverflow.com/questions/61076688/django-form-dateinput-with-widget-in-update-loosing-the-initial-value
    widgets = {
      "proBirthDate": DateInput(
        attrs={
          'class': 'form-control',
          'placeholder': 'Seleccione una fecha',
          'type': 'date'
        },
        format=('%Y-%m-%d')),
      "proEmergencyContactName": TextInput(
        attrs = {
          'placeholder': 'Nombre del contacto de menergencia'
        }),
      "proEmergencyContactTel": TextInput(
        attrs = {
          'placeholder': 'Telefono del contacto de menergencia'
        }),
      "proAlerg": Textarea(
        attrs={
          'placeholder': 'Ingrese NO si no tiene alergias',
          'style': 'height: 5rem'
        }
      ),
      "proEnfer": Textarea(
        attrs={
          'placeholder': 'Ingrese NO si no tiene enfermedades',
          'style': 'height: 5rem'
        }
      ),
      "proMedi": Textarea(
        attrs={
          'placeholder': 'Ingrese NO si no toma medicación',
          'style': 'height: 5rem'
        }
      ),
      "proRefe": Textarea(
        attrs={
          'placeholder': 'Recomendación, Red Social, etc',
          'style': 'height: 5rem'
        }
      ),
    }
    labels = {
      "proTel": "Telefono",
      "proBirthDate": "Fecha de Nacimiento",
      "proEmergencyContactName": "C. Emergencia Nombre",
      "proEmergencyContactTel": "C. Emergencia Telefono",
      "proAlerg": "Alergias",
      "proEnfer": "Enfermedad",
      "proMedi": "Medicamentos",
      "proRefe": "Referencia",
    }
    exclude = ["user", "isActive"]

class CustomUserForm(UserCreationForm):
  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)
    for visible in self.visible_fields():
      visible.field.widget.attrs['class'] = 'input-control'

  class Meta:
    model = User
    fields = ['username', 'email', 'password1', 'password2', 'first_name', 'last_name']
    widgets = {
      'username': TextInput(
        attrs = {
          'minlength': 5,
          'maxlength': 50
        }
      )
    }
    help_texts = {
      'username': 'Entre 5 y 50 caracteres permitidos'
    }

  def username_clean(self):
    username = self. cleaned_data['username'].lower()
    new = User.objects.filter(username = username)
    if new.count():
      raise ValidationError("El usuario ya existe")
    return username

  def email_clean(self):
    email = self.cleaned_data['email'].lower()
    expr = "/^\w+([\.-]?\w+)*@(?:|hotmail|outlook|yahoo|live|gmail)\.(?:|com)+$/"

    if not re.fullmatch(expr, email):
      raise ValidationError("Ingrese un email correcto")

    new = User.objects.filter(email=email)
    if new.count():
      raise ValidationError("El email ya existe")
    return email

  def clean_password2(self):
    password1 = self.cleaned_data['password1']  
    password2 = self.cleaned_data['password2']  

    if password1 and password2 and password1 != password2:  
      raise ValidationError("Las contraseñas son distintas")  
    return password2  

  def save(self, commit = True):
    user = User.objects.create_user(  
      self.cleaned_data['username'],  
      self.cleaned_data['email'],  
      self.cleaned_data['password1'], 
      self.cleaned_data['first_name'] ,
      self.cleaned_data['last_name'], 
    )
    return user

class TurnForm(ModelForm):
  class Meta:
    model = Turn
    fields = ['turDate', 'turHrFrom', 'serviceType']
    widgets = {
      'turFecha': NumberInput(
        attrs={
          'type': 'date',
          'min': date.today()
        },
      ),
      'turHrDesde': TimeInput(
        attrs={
          'type': 'time',
          'min':'08:59',
          'max':'18:00:01',
        }
      ),
    }
    labels = {
      'turDate': 'Fecha',
      'turHrTo': 'Hora desde',
      'serviceType': 'Servicio',
    }
