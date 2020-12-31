import os
import numpy as np
import matplotlib.pyplot as plt
import base64
from io import BytesIO
# from scipy.interpolate import interp


p_atm = 101.325
fi_max = 100 / 100
t_cooling = 7


def save(name='', fmt='png'):
    pwd = os.getcwd()
    i_path = f'{pwd}/pictures/{fmt}'
    if not os.path.exists(i_path):
        os.mkdir(i_path)
    os.chdir(i_path)
    plt.savefig(f'{name}.{fmt}')
    os.chdir(pwd)


def save_bytes():
    buf = BytesIO()
    plt.savefig(buf, format="png")
    data = base64.b64encode(buf.getbuffer()).decode("ascii")
    return data


def plot_id():
    d = np.linspace(0, 30, 5)
    t = [i for i in range(-25, 61, 1)]
    h = [i for i in range(-20, 131, 1)]
    fi = [i for i in range(0, 101, 1)]

    for i in t:
        if i % 2 == 0:
            izotermy = lambda x: (1.01 * i + 0.00186 * i * x) / 1.01
            plt.plot(d, izotermy(d), color='#0a0b0c', linewidth=1)

    for i in h:
        if i % 5 == 0:
            izoentalpy = lambda x: (i - x * 2.501) / 1.01
            plt.plot(d, izoentalpy(d), color='#0a0b0c', linewidth=1)

    for i in fi:
        if i % 5 == 0:
            x = np.array([(0.6222 * i / 100 * pd(j) / (p_atm - i / 100 * pd(j) / 1000)) for j in t])
            y = np.array([])

            for z in range(len(t)):
                y = np.append(y, [(1.01 * t[z] + 0.00186 * t[z] * x[z]) / 1.01])

            if i % 10 == 0:
                plt.plot(x, y, color='#0a0b0c', linewidth=1)

                if i == 100:
                    plt.plot(x, y, color='#0a0b0c', linewidth=2)

            else:
                plt.plot(x[10:], y[10:], color='#0a0b0c', linewidth=0.2)


def plot_process(t1, d1, t2, d2, tmix=None, dmix=None, process=None):
    color_process = {
        'h': 'r',
        'c': 'b',
        'p': 'g',
        'a': 'g',
        'm': 'y',
        'x': 'y'
    }

    y1 = (1.01 * t1 + 0.00186 * t1 * d1) / 1.01
    y2 = (1.01 * t2 + 0.00186 * t2 * d2) / 1.01

    if tmix is not None:
        ymix = (1.01 * tmix + 0.00186 * tmix * dmix) / 1.01
        x = np.array([d1, dmix, d2])
        y = np.array([y1, ymix, y2])

    else:
        x = np.array([d1, d2])
        y = np.array([y1, y2])

    plt.plot(x, y, color=color_process[process], linewidth=2)
    for i in range(len(x)):
        plt.scatter(x[i], y[i], color=color_process[process])


def found_dt(t=None, fi=None, d=None, h=None):
    # 1 - we have t d
    if t is not None and d is not None:
        t, d = t, d
        h = 1.01 * t + (2501 + 1.86 * t) * d / 1000
    # 2 - we have t fi
    elif t is not None and fi is not None:
        d = 0.6222 * fi / 100 * pd(t) / (p_atm - fi / 100 * pd(t) / 1000)
        h = 1.01 * t + (2501 + 1.86 * t) * d / 1000
    # 3 - we have h d
    elif h is not None and d is not None:
        t1 = (h - 2501 * d / 1000) / (1.01 + 1.86 * d / 1000)
        t2 = -25
        while True:
            d1 = 0.6222 * fi_max * pd(t2) / (p_atm - fi_max * pd(t2) / 1000)
            d2 = (h - 1.01 * t2) / (2501 + 1.86 * t2) * 1000
            if abs(d1 - d2) < 0.001:
                break
            else:
                t2 += 0.001
        t = t1 if t1 > t2 else t2
        if h == 0 and d == 0:
            d = 0
        else:
            d = d1

    # 4 - we have t h
    elif t is not None and h is not None:
        d = min((h - 1.01 * t) / (2501 + 1.86 * t) * 1000, max_d(t))
    # 5 - we have fi d
    elif fi is not None and d is not None:
        fi = min(fi / 100, fi_max)
        pard = d / 1000 * p_atm / fi / (0.6222 + d / 1000) * 1000
        if pard < 641:
            t = (271 * np.log(pard) - 1738.4) / (28.74 - np.log(pard))
        else:
            t = (234 * np.log(pard) - 1500.3) / (23.5 - np.log(pard))
        h = 1.01 * t + (2501 + 1.86 * t) * d / 1000
    # 6 - we have fi h
    elif fi is not None and h is not None:
        t1 = -25
        while True:
            d1 = 0.6222 * fi / 100 * pd(t1) / (p_atm - fi / 100 * pd(t1) / 1000)
            d2 = (h - 1.01 * t1) / (2501 + 1.86 * t1) * 1000
            if abs(d1 - d2) < 0.001:
                break
            else:
                t1 += 0.001
        t, d = t1, d1

    fi = 100 * p_atm / pd(t) * 1000 / (0.6222 / d * 1000 + 1)

    t_m = 0

    return {
        't': t,
        'd': d,
        'h': h,
        'fi': fi,
        't_m': t_m
    }


def pd(t):
    if t < -50:
        result = None
    elif t < 0:
        result = np.exp((1738.4 + 28.74 * t) / (271 + t))
    elif t < 100:
        result = np.exp((1500.3 + 23.5 * t) / (234 + t))
    else:
        result = None
    return result


def max_d(t):
    return 0.6222 * fi_max * pd(t) / (p_atm - fi_max * pd(t) / 1000)


# process
def heat(t1, fi1, flow, t2=None, power=None):
    process = 'h'
    g = flow / 3600 * 1.2
    point_1 = found_dt(t=t1, fi=fi1)
    d2 = point_1['d']

    if t2 is not None:
        point_2 = found_dt(t=t2, d=d2)
        power = g * (point_2['h'] - point_1['h'])

    elif power is not None:
        h2 = point_1['h'] + power / g
        point_2 = found_dt(d=d2, h=h2)
        t2 = point_2['t']

    humidity_inflow = g * (point_2['d'] - point_1['d']) * 3.6

    plot_process(t1=point_1['t'], d1=point_1['d'], t2=point_2['t'], d2=point_2['d'], process=process)

    return {
        't1': round(point_1['t']),
        'fi1': round(point_1['fi']),
        'd1': round(point_1['d'], 2),
        'h1': round(point_1['h']),
        'flow': flow,
        't2': round(t2),
        'fi2': round(point_2['fi']),
        'd2': round(point_2['d'], 2),
        'h2': round(point_2['h']),
        'power': round(power, 2),
        'humidity_inflow': round(humidity_inflow, 2),
        'process': process
    }


def cooling(t1, fi1, flow, t2=None, power=None):
    process = 'c'
    d_surface_cooler = 0.6222 * pd(t_cooling) / (p_atm - pd(t_cooling) / 1000)
    h_surface_cooler = 1.01 * t_cooling + (2501 + 1.86 * t_cooling) * d_surface_cooler / 1000
    g = flow / 3600 * 1.2
    point_1 = found_dt(t=t1, fi=fi1)

    if t2 is not None:
        if d_surface_cooler < point_1['d']:
            h2 = point_1['h'] - (point_1['h'] - h_surface_cooler) * (t2 - t1) / (t_cooling - t1)
        d2 = (h2 - 1.01 * t2) / (2501 + 1.86 * t2) * 1000
        point_2 = found_dt(t=t2, d=d2)
        power = g * (point_2['h'] - point_1['h'])

    elif power is not None:
        h2 = point_1['h'] - power / g
        d2 = min(point_1['d'], point_1['d'] + (d_surface_cooler - point_1['d']) * (point_1['h'] - h2) / (
                    point_1['h'] - h_surface_cooler))
        point_2 = found_dt(d=d2, h=h2)
        t2 = point_2['t']

    humidity_inflow = g * (point_2['d'] - point_1['d']) * 3.6

    plot_process(t1=point_1['t'], d1=point_1['d'], t2=point_2['t'], d2=point_2['d'], process=process)

    return {
        't1': round(point_1['t']),
        'fi1': round(point_1['fi']),
        'd1': round(point_1['d'], 2),
        'h1': round(point_1['h']),
        'flow': flow,
        't2': round(t2),
        'fi2': round(point_2['fi']),
        'd2': round(point_2['d'], 2),
        'h2': round(point_2['h']),
        'power': round(power, 2),
        'humidity_inflow': round(humidity_inflow, 2),
        'process': process
    }


def adiabatic_humidification(t1, fi1, flow, t2=None, fi2=None, d2=None):
    process = 'a'
    point_1 = found_dt(t=t1, fi=fi1)
    g = flow / 3600 * 1.2
    h2 = point_1['h']

    if t2 is not None:
        point_2 = found_dt(t=t2, h=h2)

    elif fi2 is not None:
        point_2 = found_dt(fi=fi2, h=h2)
    elif d2 is not None:
        point_2 = found_dt(d=d2, h=h2)

    power = g * (point_2['h'] - point_1['h'])
    humidity_inflow = g * (point_2['d'] - point_1['d']) * 3.6

    plot_process(t1=point_1['t'], d1=point_1['d'], t2=point_2['t'], d2=point_2['d'], process=process)

    return {
        't1': round(point_1['t']),
        'fi1': round(point_1['fi']),
        'd1': round(point_1['d'], 2),
        'h1': round(point_1['h']),
        'flow': flow,
        't2': round(point_2['t']),
        'fi2': round(point_2['fi']),
        'd2': round(point_2['d'], 2),
        'h2': round(point_2['h']),
        'power': round(power, 2),
        'humidity_inflow': round(humidity_inflow, 2),
        'process': process
    }


def humidification(t1, fi1, flow, fi2=None, d2=None):
    process = 'p'
    point_1 = found_dt(t=t1, fi=fi1)
    g = flow / 3600 * 1.2
    t2 = t1

    if fi2 is not None:
        point_2 = found_dt(fi=fi2, t=t2)
    elif d2 is not None:
        d2 = d2 if d2 <= max_d(t2) else max_d(t2)
        point_2 = found_dt(d=d2, t=t2)

    power = g * (point_2['h'] - point_1['h'])
    humidity_inflow = g * (point_2['d'] - point_1['d']) * 3.6

    plot_process(t1=point_1['t'], d1=point_1['d'], t2=point_2['t'], d2=point_2['d'], process=process)

    return {
        't1': round(point_1['t']),
        'fi1': round(point_1['fi']),
        'd1': round(point_1['d'], 2),
        'h1': round(point_1['h']),
        'flow': flow,
        't2': round(point_2['t']),
        'fi2': round(point_2['fi']),
        'd2': round(point_2['d'], 2),
        'h2': round(point_2['h']),
        'power': round(power, 2),
        'humidity_inflow': round(humidity_inflow, 2),
        'process': process
    }


def mixing(t1, fi1, flow1, t2, fi2, flow2):
    process = 'm'
    point_1 = found_dt(t=t1, fi=fi1)
    point_2 = found_dt(t=t2, fi=fi2)
    flow_mix = flow1 + flow2
    g_1 = flow1 / 3600 * 1.2
    g_2 = flow2 / 3600 * 1.2
    g_mix = g_1 + g_2
    d_mix = (point_1['d'] * g_1 + g_2 * point_2['d']) / g_mix
    h_mix = (point_1['h'] * g_1 + g_2 * point_2['h']) / g_mix
    point_mix = found_dt(d=d_mix, h=h_mix)
    if d_mix < point_mix['d']:
        point_mix['d'] = d_mix

    humidity_inflow = (g_mix * point_mix['d'] - g_2 * point_2['d'] - g_1 * point_1['d']) * 3.6

    plot_process(t1=point_1['t'], d1=point_1['d'], t2=point_2['t'], d2=point_2['d'],
                 tmix=point_mix['t'], dmix=point_mix['d'], process=process)

    return {
        't1': round(point_1['t']),
        'fi1': round(point_1['fi']),
        'd1': round(point_1['d'], 2),
        'h1': round(point_1['h']),
        't2': round(point_2['t']),
        'fi2': round(point_2['fi']),
        'd2': round(point_2['d'], 2),
        'h2': round(point_2['h']),
        'tmix': round(point_mix['t']),
        'fimix': round(point_mix['fi']),
        'dmix': round(point_mix['d'], 2),
        'hmix': round(point_mix['h']),
        'flow_mix': flow_mix,
        'humidity_inflow': round(humidity_inflow, 2),
        'process': process
    }


def process_x(t1, fi1, d1, h1, t2, fi2, d2, h2, flow):
    pass


if __name__ == '__main__':

    plt.subplots(figsize=(6, 10))
    plt.axis([0, 30, -25, 55])
    plot_id()

    z = heat(t1=-22, fi1=95, flow=1000, t2=24)
    print(z)

    # plt.grid(True)
    save(name='pic_2_1', fmt='png')
    save_bytes()

    plt.show()
