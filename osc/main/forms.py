from .models import Oscilloscope, SignalGenerator, Power
from django.forms import ModelForm, TextInput, PasswordInput
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User


# not used because it doesn't actually style forms
class LoginForm(AuthenticationForm):
    class Meta:
        model = User
        fields = ['username', 'password']
        widgets = {
            "username": TextInput(attrs={
                'type': 'text',
                'id': 'username',
                'class': 'form-control',
                'placeholder': 'username',
                'required': 'required',
                'autofocus': 'autofocus'
            }),
            "password": PasswordInput(attrs={
                'type': 'password',
                'id': 'password',
                'class': 'form-control',
                'placeholder': 'password',
                'required': 'required'
            })
        }

class GeneratorForm(ModelForm):
    class Meta:
        model = SignalGenerator
        fields = ("channel", "sig_form", "frequency", "amplitude")


class ScopeForm(ModelForm):
    class Meta:
        model = Oscilloscope
        # fields = ("show_graph","ch_scale","time_base","offset_x","offset_y","show_graph2","ch_scale2","offset_x2","offset_y2","show_graph3","ch_scale3","offset_x3","offset_y3","show_graph4","ch_scale4","offset_x4","offset_y4")
        fields = ("show_graph","ch_scale","time_base","offset_x","offset_y","show_graph2","ch_scale2","time_base2","offset_x2","offset_y2","show_graph3","ch_scale3","time_base3","offset_x3","offset_y3","show_graph4","ch_scale4","time_base4","offset_x4","offset_y4")

class PowerForm(ModelForm):
    class Meta:
        model = Power
        fields = ("power_channel","voltage")

# class ScopeForm(ModelForm):
#     class Meta:
#         model = Oscilloscope
#         fields = ("ch_scale","time_base")