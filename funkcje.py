import pandas as pd
from pyproj import Transformer
import math
import csv

transformacja = Transformer.from_crs(2180, 2178)
tt = transformacja.transform
trans2000na192 = Transformer.from_crs(2178, 2180)
tt2 = trans2000na192.transform


def godlo_2000_10k(u2000):
    """(x2000, y2000)"""
    godlo_1 = math.floor(u2000[1] / 1e6)
    godlo_2 = math.floor((u2000[0] / 1e3 - 4920) / 5)
    godlo_3 = math.floor(((u2000[1] - godlo_1 * 1e6) / 1e3 - 332) / 8)
    godlo = str(godlo_1) + '_' + str(godlo_2) + '_' + str(godlo_3)
    return godlo


"""petla, funkcja tylko  (plik wsadowy, 
        podczyt z pliku 
        przelicznie wsp
        zapis do pliku zgodnie z godłęm mapy 1:10 000"""
root_path = 'C:/Users/olexs/PycharmProjects/model_1992_na_2000/'
dane = 'input/xyh1992.csv'

yx = pd.read_csv(root_path + dane, header=None, sep=None, engine='python', names=['X1992', 'Y19992', 'Z'])
print(yx)


def x1992_do_x2000(xyh):
    xy = tt(xyh[0], xyh[1])
    xyh['X2000'] = format(xy[0], "^-9.3f")
    xyh['Y2000'] = format(xy[1], "^-9.3f")
    xyh['godlo2000'] = godlo_2000_10k(xy)
    return xyh


def x2000_do_x1992(xyh):
    xy = tt2(xyh[0], xyh[1])
    xyh[0] = format(xy[0], "^-9.3f")
    xyh[1] = format(xy[1], "^-9.3f")
    #  print(godlo_2000_10k(xy))
    return xyh

yx.apply(x1992_do_x2000, axis=1)  #
print(yx)
# print(yx2000)
#with open('C:\Users\olexs\PycharmProjects\model_1992_na_2000\ouput\wyn.csv', 'w', newline='') as csvfile_w:
#    spamwriter = csv.writer(csvfile_w, delimiter='\t', quotechar='|', quoting=csv.QUOTE_MINIMAL)
#    spamwriter.writerow(f'{yx[0]:.3f}\t{yx[1]:.3f}\t{yx[2]}')

# 5695850+100 7570300+100
z = {'X': [5695850.00, 5695850.00, 5695950.00, 5695950.0], 'Y': [7570300.0, 7570400.0, 7570300.0, 7570400.0]}
xz = pd.DataFrame(data=z)
xz1992 = xz.apply(x2000_do_x1992, axis=1)
#yx1 = pd.read_csv(root_path + dane, header=None, sep=None, engine='python', names=['X', 'Y', 'Z'])
