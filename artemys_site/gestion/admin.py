from django.contrib import admin

from gestion.models import Profile, Comment, Turn, ServiceType

admin.site.register(Profile)
admin.site.register(Comment)
admin.site.register(ServiceType)
admin.site.register(Turn)
