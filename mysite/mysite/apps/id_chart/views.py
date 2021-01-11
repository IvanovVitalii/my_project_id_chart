import os
from django.http import HttpResponse
from datetime import datetime

from .maths_id_chart import *


def index(request):

    plt.subplots(figsize=(6, 10))
    plt.axis([0, 30, -25, 55])
    plot_id()

    z0 = cooling(t1=32, fi1=40, flow=1000, t2=20)
    z1 = heat(t1=z0['t2'], fi1=z0['fi2'], flow=z0['flow'], t2=40)
    z2 = humidification(t1=z1['t2'], fi1=z1['fi2'], flow=z1['flow'], fi2=40)

    data = save_bytes()

    return HttpResponse(f'process 1:{z0["process"]}, '
                        f't1={z0["t1"]}, '
                        f't2={z0["t2"]}, '
                        f'flow={z0["flow"]}, '
                        f'power: {z0["power"]} kW '
                        '<br>'
                        f'process 2:{z1["process"]}, '
                        f't1={z1["t1"]}, '
                        f't2={z1["t2"]}, '
                        f'flow={z1["flow"]}, '
                        f'power: {z1["power"]} kW '
                        '<br>'
                        f'process 3:{z2["process"]}, '
                        f'fi1={z2["fi1"]}, '
                        f'fi2={z2["fi2"]}, '
                        f'd1={z2["d1"]}, '
                        f'd2={z2["d2"]}, '
                        f'flow={z2["flow"]}, '
                        f'power: {z2["power"]} kW, '
                        f'humidity inflow: {z2["humidity_inflow"]} kg '
                        '<br>'
                        f"<img src='data:image/png;base64,{data}'/>")
