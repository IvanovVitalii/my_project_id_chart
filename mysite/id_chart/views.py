import os
from django.http import HttpResponse
from datetime import datetime

from .maths_id_chart import *


def index(request):

    plt.subplots(figsize=(6, 10))
    plt.axis([0, 30, -25, 55])
    plot_id()

    z = cooling(t1=32, fi1=40, flow=1000, t2=20)
    z1 = heat(t1=z['t2'], fi1=z['fi2'], flow=z['flow'], t2=40)

    data = save_bytes()

    return HttpResponse(f'process 1:{z["process"]}, power: {z["power"]} kW \n'
                        f'process 2:{z1["process"]}, power: {z1["power"]} kW\n'
                        f"<img src='data:image/png;base64,{data}'/>")
