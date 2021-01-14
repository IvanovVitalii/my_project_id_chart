from django.http import Http404
from django.shortcuts import render
from django.http import HttpResponse
from .maths_id_chart import *


def index(request, flow=100):
    if 'flow' in request.GET:
        context = {}
        flow = int(request.GET['flow'])

        plt.subplots(figsize=(6, 10))
        plt.axis([0, 30, -25, 55])
        plot_id()

        z0 = humidification(t1=24, fi1=3, flow=flow, fi2=60)
        points = 1
        point = [i + 1 for i in range(points)]

        data = save_bytes()

        id_image = f'data:image/png;base64,{data}'
    else:
        plt.subplots(figsize=(6, 10))
        plt.axis([0, 30, -25, 55])
        plot_id()

        z0 = humidification(t1=0, fi1=0, flow=0, fi2=0)
        points = 1
        point = [i + 1 for i in range(points)]

        data = save_bytes()

        id_image = f'data:image/png;base64,{data}'

    context = {
        'point': point,
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
