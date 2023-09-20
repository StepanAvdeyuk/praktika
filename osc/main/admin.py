from django.contrib import admin
from .models import Oscilloscope, SignalGenerator, Power

admin.site.register(Oscilloscope)
admin.site.register(SignalGenerator)
admin.site.register(Power)