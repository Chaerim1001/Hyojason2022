from django.contrib import admin
from .models import App
from .models import Guideline

# Register your models here.

admin.site.register(App)
admin.site.register(Guideline)