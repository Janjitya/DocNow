from django.contrib import admin
from .models import Profile, Doctor, Appiontment

# Register your models here.
admin.site.register(Profile)
admin.site.register(Doctor)
admin.site.register(Appiontment)
