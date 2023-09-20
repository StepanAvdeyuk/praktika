from django.shortcuts import render, redirect
from .models import Oscilloscope, SignalGenerator, Power
from .forms import ScopeForm, GeneratorForm, PowerForm
from django.http import JsonResponse
from django.forms.models import model_to_dict
from django.views.generic import View
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

import pyvisa
import matplotlib.pyplot as plot
import math
import numpy
import time as timee

# import warnings
# warnings.filterwarnings("ignore")

from io import StringIO

def mod_appliances(request): 
    rm = pyvisa.ResourceManager()

    # из доступных usb вибраются нужные
    scope_usb = list(filter(lambda x: 'DS1ZD204101021' in x, rm.list_resources()))
    generator_usb = list(filter(lambda x: 'DG1ZA202603185' in x, rm.list_resources()))
    power_usb = list(filter(lambda x: 'DP8B214501324' in x, rm.list_resources()))

    # открываем подключенное оборудование для управления
    scope = rm.open_resource(scope_usb[0])
    generator = rm.open_resource(generator_usb[0])
    power = rm.open_resource(power_usb[0])

    # команда отправляет команду на генератор сигналов, чтобы установить значения
    generator.write(f'{request["channel"]}:APPL:{request["sig_form"]} {request["frequency"]},{request["amplitude"]}')

    power.write(f':APPL {request["power_channel"]},{request["voltage"]}')
    power.close()

    # запуск и установка значений осцилографу 
    scope.write(":RUN")

    scope.write(f':TIMebase:SCALe CH1,{request["time_base"]}')
    scope.write(f':TIMebase:SCALe CH2,{request["time_base2"]}')
    scope.write(f':TIMebase:SCALe CH3,{request["time_base3"]}')
    scope.write(f':TIMebase:SCALe CH4,{request["time_base4"]}')

    
    scope.write(f':CHANnel1:SCALe {request["ch_scale"]}')
    scope.write(f':CHANnel2:SCALe {request["ch_scale2"]}')
    scope.write(f':CHANnel3:SCALe {request["ch_scale3"]}')
    scope.write(f':CHANnel4:SCALe {request["ch_scale4"]}')
       
    # установка смещений  
    scope.write(f':CHANnel1:OFFSet {request["offset_y"]}') 
    scope.write(f':CHANnel2:OFFSet {request["offset_y2"]}') 
    scope.write(f':CHANnel3:OFFSet {request["offset_y3"]}') 
    scope.write(f':CHANnel4:OFFSet {request["offset_y4"]}') 

    scope.write(f':TIMebase:POSition CH1,{request["offset_x"]}')  
    scope.write(f':TIMebase:POSition CH2,{request["offset_x2"]}')  
    scope.write(f':TIMebase:POSition CH3,{request["offset_x3"]}')  
    scope.write(f':TIMebase:POSition CH4,{request["offset_x4"]}')  

    timee.sleep(0.5)
    scope.write(":STOP")
    
    scope.close()


def return_graph(request):
    # Создание объекта ResourceManager и открытие ресурса осциллоскопа:
    rm = pyvisa.ResourceManager()
    scope = rm.open_resource('USB0::0x1AB1::0x04CE::DS1ZD204101021::INSTR')

    if (request["show_graph"] == "TRUE"): 
                # Запуск и остановка осциллоскопа
        scope.write(":RUN")
        timee.sleep(2)
        scope.write(":STOP")

        # Получение параметров измерений
        sample_rate = scope.query_ascii_values(':ACQ:SRAT?')[0]
        scope.write(":WAV:SOUR CHAN1")
        YORigin = scope.query_ascii_values(":WAV:YOR?")[0]
        YREFerence = scope.query_ascii_values(":WAV:YREF?")[0]
        YINCrement = scope.query_ascii_values(":WAV:YINC?")[0]
        XORigin = scope.query_ascii_values(":WAV:XOR?")[0]
        XREFerence = scope.query_ascii_values(":WAV:XREF?")[0]
        XINCrement = scope.query_ascii_values(":WAV:XINC?")[0]
        time_base = scope.query_ascii_values(":TIM:SCAL?")[0]
        memory_depth = (time_base*12) * sample_rate
        scope.write(":WAV:MODE RAW")
        scope.write(":WAV:FORM BYTE")
        scope.write(":WAV:STAR 1")
        scope.write(":WAV:STOP 250000")

        # Получение данных с осциллоскопа
        rawdata = scope.query_binary_values(":WAV:DATA?", datatype='B')
        if (memory_depth > 250000):
            loopcount = 1
            loopmax = math.ceil(memory_depth/250000)
            while (loopcount < loopmax):
                start = (loopcount*250000)+1
                scope.write(":WAV:STAR {0}".format(start))
                stop = (loopcount+1)*250000
                scope.write(":WAV:STOP {0}".format(stop))
                rawdata.extend(scope.query_binary_values(":WAV:DATA?", datatype='B'))
                loopcount = loopcount+1
        scope.write(":MEAS:SOUR CHAN1")
        scope.close()

        # Обработка данных и создание графика:
        data = (numpy.asarray(rawdata) - YORigin - YREFerence) * YINCrement
        data_size = len(data)
        time = numpy.linspace(XREFerence, XINCrement * data_size, data_size)
        if (time[-1] < 1e-3):
            time = time * 1e6
            tUnit = "uS"
        elif (time[-1] < 1):
            time = time * 1e3
            tUnit = "mS"
        else:
            tUnit = "S"

    if (request["show_graph2"] == "TRUE"):

        # 2 канал

        scope = rm.open_resource('USB0::0x1AB1::0x04CE::DS1ZD204101021::INSTR')

        # Запуск и остановка осциллоскопа 2
        scope.write(":RUN")
        timee.sleep(2)
        scope.write(":STOP")

        # Получение параметров измерений 2
        sample_rate2 = scope.query_ascii_values(':ACQ:SRAT?')[0]
        scope.write(":WAV:SOUR CHAN2")
        YORigin2 = scope.query_ascii_values(":WAV:YOR?")[0]
        YREFerence2= scope.query_ascii_values(":WAV:YREF?")[0]
        YINCrement2 = scope.query_ascii_values(":WAV:YINC?")[0]
        XORigin2 = scope.query_ascii_values(":WAV:XOR?")[0]
        XREFerence2 = scope.query_ascii_values(":WAV:XREF?")[0]
        XINCrement2 = scope.query_ascii_values(":WAV:XINC?")[0]
        time_base2 = scope.query_ascii_values(":TIM:SCAL?")[0]
        memory_depth2 = (time_base2*12) * sample_rate2
        scope.write(":WAV:MODE RAW")
        scope.write(":WAV:FORM BYTE")
        scope.write(":WAV:STAR 1")
        scope.write(":WAV:STOP 250000")

        # Получение данных с осциллоскопа 2
        rawdata2 = scope.query_binary_values(":WAV:DATA?", datatype='B')
        if (memory_depth2 > 250000):
            loopcount = 1
            loopmax = math.ceil(memory_depth/250000)
            while (loopcount < loopmax):
                start = (loopcount*250000)+1
                scope.write(":WAV:STAR {0}".format(start))
                stop = (loopcount+1)*250000
                scope.write(":WAV:STOP {0}".format(stop))
                rawdata2.extend(scope.query_binary_values(":WAV:DATA?", datatype='B'))
                loopcount = loopcount+1
        scope.write(":MEAS:SOUR CHAN2")
        scope.close()

        # Обработка данных и создание графика 2:
        data2 = (numpy.asarray(rawdata2) - YORigin2 - YREFerence2) * YINCrement2
        data_size2 = len(data2)
        time2 = numpy.linspace(XREFerence2, XINCrement2 * data_size2, data_size2)
        if (time2[-1] < 1e-3):
            time2 = time2 * 1e6
            tUnit = "uS"
        elif (time2[-1] < 1):
            time2 = time2 * 1e3
            tUnit = "mS"
        else:
            tUnit = "S"


    if (request["show_graph3"] == "TRUE"):

        # 3 канал

        scope = rm.open_resource('USB0::0x1AB1::0x04CE::DS1ZD204101021::INSTR')

        # Запуск и остановка осциллоскопа 3
        scope.write(":RUN")
        timee.sleep(2)
        scope.write(":STOP")

        # Получение параметров измерений 3
        sample_rate3 = scope.query_ascii_values(':ACQ:SRAT?')[0]
        scope.write(":WAV:SOUR CHAN3")
        YORigin3 = scope.query_ascii_values(":WAV:YOR?")[0]
        YREFerence3= scope.query_ascii_values(":WAV:YREF?")[0]
        YINCrement3 = scope.query_ascii_values(":WAV:YINC?")[0]
        XORigin3 = scope.query_ascii_values(":WAV:XOR?")[0]
        XREFerence3 = scope.query_ascii_values(":WAV:XREF?")[0]
        XINCrement3 = scope.query_ascii_values(":WAV:XINC?")[0]
        time_base3 = scope.query_ascii_values(":TIM:SCAL?")[0]
        memory_depth3 = (time_base3*12) * sample_rate3
        scope.write(":WAV:MODE RAW")
        scope.write(":WAV:FORM BYTE")
        scope.write(":WAV:STAR 1")
        scope.write(":WAV:STOP 250000")

        # Получение данных с осциллоскопа 3
        rawdata3 = scope.query_binary_values(":WAV:DATA?", datatype='B')
        if (memory_depth3 > 250000):
            loopcount = 1
            loopmax = math.ceil(memory_depth/250000)
            while (loopcount < loopmax):
                start = (loopcount*250000)+1
                scope.write(":WAV:STAR {0}".format(start))
                stop = (loopcount+1)*250000
                scope.write(":WAV:STOP {0}".format(stop))
                rawdata3.extend(scope.query_binary_values(":WAV:DATA?", datatype='B'))
                loopcount = loopcount+1
        scope.write(":MEAS:SOUR CHAN3")
        scope.close()

        # Обработка данных и создание графика 3:
        data3 = (numpy.asarray(rawdata3) - YORigin3 - YREFerence3) * YINCrement3
        data_size3 = len(data3)
        time3 = numpy.linspace(XREFerence3, XINCrement3 * data_size3, data_size3)
        if (time3[-1] < 1e-3):
            time3 = time3 * 1e6
            tUnit = "uS"
        elif (time3[-1] < 1):
            time3 = time3 * 1e3
            tUnit = "mS"
        else:
            tUnit = "S"

    if (request["show_graph4"] == "TRUE"):

        # 4 канал

        scope = rm.open_resource('USB0::0x1AB1::0x04CE::DS1ZD204101021::INSTR')

        # Запуск и остановка осциллоскопа 4
        scope.write(":RUN")
        timee.sleep(2)
        scope.write(":STOP")

        # Получение параметров измерений 4
        sample_rate4 = scope.query_ascii_values(':ACQ:SRAT?')[0]
        scope.write(":WAV:SOUR CHAN4")
        YORigin4 = scope.query_ascii_values(":WAV:YOR?")[0]
        YREFerence4= scope.query_ascii_values(":WAV:YREF?")[0]
        YINCrement4 = scope.query_ascii_values(":WAV:YINC?")[0]
        XORigin4 = scope.query_ascii_values(":WAV:XOR?")[0]
        XREFerence4 = scope.query_ascii_values(":WAV:XREF?")[0]
        XINCrement4 = scope.query_ascii_values(":WAV:XINC?")[0]
        time_base4 = scope.query_ascii_values(":TIM:SCAL?")[0]
        memory_depth4 = (time_base4*12) * sample_rate4
        scope.write(":WAV:MODE RAW")
        scope.write(":WAV:FORM BYTE")
        scope.write(":WAV:STAR 1")
        scope.write(":WAV:STOP 250000")

        # Получение данных с осциллоскопа 4
        rawdata4 = scope.query_binary_values(":WAV:DATA?", datatype='B')
        if (memory_depth4 > 250000):
            loopcount = 1
            loopmax = math.ceil(memory_depth/250000)
            while (loopcount < loopmax):
                start = (loopcount*250000)+1
                scope.write(":WAV:STAR {0}".format(start))
                stop = (loopcount+1)*250000
                scope.write(":WAV:STOP {0}".format(stop))
                rawdata4.extend(scope.query_binary_values(":WAV:DATA?", datatype='B'))
                loopcount = loopcount+1
        scope.write(":MEAS:SOUR CHAN4")
        scope.close()

        # Обработка данных и создание графика 4:
        data4 = (numpy.asarray(rawdata4) - YORigin4 - YREFerence4) * YINCrement4
        data_size4 = len(data4)
        time4 = numpy.linspace(XREFerence4, XINCrement4 * data_size4, data_size4)
        if (time4[-1] < 1e-3):
            time4 = time4 * 1e6
            tUnit = "uS"
        elif (time4[-1] < 1):
            time4 = time4 * 1e3
            tUnit = "mS"
        else:
            tUnit = "S"

    # построение итогового графика
    
    fig = plot.figure()
    if (request["show_graph"] == "TRUE"): 
        plot.plot(time, data, label="Channel 1")
    if (request["show_graph2"] == "TRUE"): 
        plot.plot(time, data2, label="Channel 2")
    if (request["show_graph3"] == "TRUE"): 
        plot.plot(time, data3, label="Channel 3")
    if (request["show_graph4"] == "TRUE"): 
        plot.plot(time, data4, label="Channel 4")
    plot.ylabel("Voltage (V)")
    plot.xlabel("Time (" + tUnit + ")")
    plot.grid()
    plot.xlim(time[0], time[-1])
    plot.subplots_adjust(left=0.1, top=0.98, bottom=0.1, right=0.8)
    plot.legend()  # Добавляем легенду для обозначения каналов

     # Сохранение графика в формате SVG и возврат данных
    imgdata = StringIO()
    fig.savefig(imgdata, format='svg')
    imgdata.seek(0)
    data = imgdata.getvalue()
    return data



def home_page(request):
    return render(request, 'main/index.html')


class Scope(View):
    def get(self, request):
        print('get')
        form = ScopeForm()
        form2 = GeneratorForm()
        form3 = PowerForm()
        context = {
            'form': form,
            'form2': form2,
            'form3': form3
            }
        return render(request, 'main/scope.html', context=context)

    def post(self, request):
        print('post')
        form = ScopeForm(request.POST)
        form2 = GeneratorForm(request.POST)
        form3 = PowerForm(request.POST)
        context = {
            'form': form,
            'form2': form2,
            'form3': form3
            }
        # if form.is_valid() and form2.is_valid() and form3.is_valid():
        if (1):
            mod_appliances(request.POST)
            context['graph'] = return_graph(request.POST)
        return render(request, 'main/scope.html', context=context)


def login_page(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.info(request, 'username or password is incorrect')
    context = {'form': AuthenticationForm}
    return render(request, 'main/login.html', context)


def logout_page(request):
    logout(request)
    return redirect('home')


def reset_page(request):
    return redirect('home')


def donut_page(request):
    return render(request, 'main/donut.html')
