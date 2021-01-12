from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from .maths_id_chart import *


def index(request, flow=None, process=None, t1=None, fi1=None, d1=None, h1=None):

    plt.subplots(figsize=(6, 10))
    plt.axis([0, 30, -25, 55])
    plot_id()

    z0 = cooling(t1=32, fi1=40, flow=1000, t2=20)

    data = save_bytes()

    id_image = f'data:image/png;base64,{data}'

    context = {
        'flow': z0['flow'],
        't1': z0['t1'],
        'fi1': z0['fi1'],
        'd1': z0['d1'],
        'h1': z0['h1'],
        'process': z0['process'],
        't2': z0['t2'],
        'fi2': z0['fi2'],
        'd2': z0['d2'],
        'h2': z0['h2'],
        'power': z0['power'],
        'humidity_inflow': z0['humidity_inflow'],
        'id_image': id_image
    }

    return render(request, 'id_chart/id_chart.html', context=context)
