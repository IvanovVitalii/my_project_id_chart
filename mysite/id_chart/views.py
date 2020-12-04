import os
from django.http import HttpResponse
from datetime import datetime

from .maths_id_chart import *


def index(request):

    z = cooling(t1=32, fi1=40, flow=1000, t2=22)
    z1 = heat(t1=z['t2'], fi1=z['fi2'], flow=z['flow'], t2=30)

    filename = datetime.now().strftime("%Y%m%d-%H%M%S")
    save(name=filename, fmt='png')

    return HttpResponse(f'process 1:{z["process"]}, power: {z["power"]} kW \b'
                        f'process 2:{z1["process"]}, power: {z1["power"]} kW')
