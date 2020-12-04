from mysite.id_chart.maths_id_chart import *
from datetime import datetime


z = cooling(t1=32, fi1=40, flow=1000, t2=22)
z1 = heat(t1=z['t2'], fi1=z['fi2'], flow=z['flow'], t2=30)
filename = datetime.now().strftime("%Y%m%d-%H%M%S")

save(name=filename, fmt='png')
