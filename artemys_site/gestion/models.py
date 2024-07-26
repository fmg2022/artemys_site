from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

class Profile (models.Model):
  proTel = models.CharField(max_length=20)
  proBirthDate = models.DateField(null=True, blank=True)
  proEmergencyContactName = models.CharField(max_length=50)
  proEmergencyContactTel = models.CharField(max_length=20)

  proAlerg = models.CharField(max_length=250, help_text="Ingrese NO si no tiene alergias")
  proEnfer = models.CharField(max_length=250, help_text="Ingrese NO si no tiene enfermedades")
  proMedi = models.CharField(max_length=250, help_text="Ingrese NO si no toma medicación")
  proRefe = models.CharField(max_length=250, help_text="Recomendación, Red Social, etc")

  user = models.OneToOneField(User, on_delete=models.CASCADE)

  def get_absolute_url(self):
      return reverse("perfilInfo", kwargs={"pk": self.pk})
  

  def __str__(self):
    return self.user.last_name + ', ' + self.user.first_name
  
class Comment (models.Model):
  comContent = models.TextField(max_length=500, null=True, blank=True)
  comDateTime = models.DateTimeField(auto_now_add=True, null=True, blank=True)

  profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

  class Meta:
    ordering = ['comDateTime']

  def __str__(self):
    return self.comContent

class ServiceType(models.Model):
  serName = models.CharField(max_length=50, help_text="Ingrese el nombre del sero de Servicio")
  serDesc = models.TextField(max_length=500, help_text="Breve descripcion del Servicio por hacer")
  serTime = models.TimeField(help_text='Formato: 09:15:00  Tiempo que le toma en promedio en realizar el Servicio.', null=True, blank=True)

  def get_absolute_url(self):
    return reverse("servicio", kwargs={"pk": self.pk})

  def __str__(self):
    return self.serName

class Turn(models.Model):
  turDate = models.DateField()
  turHrFrom = models.TimeField()
  turHrTo = models.TimeField()
  turSenia = models.FloatField(default=0, null=True, blank=True)

  serviceType = models.ForeignKey(ServiceType, on_delete=models.SET_NULL, null=True)
  profile = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)

  def get_absolute_url(self):
      return reverse("turnoInfo", kwargs={"pk": self.pk})

  def __str__(self):
    self.turDate
