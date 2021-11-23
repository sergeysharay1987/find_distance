import os
import geopy
import matplotlib
import geopandas
from geopandas import GeoDataFrame
from matplotlib import pyplot as plt
import requests
from matplotlib.pyplot import plot, show
from openpyxl import Workbook, load_workbook
from geopandas.tools import geocode
from geopy.geocoders import Yandex
from shapely.geometry import Polygon, Point
from shapely.ops import nearest_points
from geopy.distance import geodesic, distance

API_KEY = 'cbddbd2c-95ce-4aa1-ba5a-5d0416597c20'
number_of_mkad_s_kms = 108  # кол-во километров МКАД
mkad_address = 'Russia Moscow MKAD'  # неизменяющееся часть адреса МКАД
number_of_km = 0  # номер километра МКАД, начиная с нулевого
coords_for_polygon_mkad = []

excel_file = 'coords_of_mkad_s_kms.xlsx'

list_mkad_s_km = []  # список, для хранения координат каждого километра МКАД

list_of_addresses_for_request = []  # список, содержащий urls для HTTP-запросов на геокодирование


def make_list_of_addresses_for_request():
    """Возвращает строку, содержащую адреса всех километров МКАД, разделённых запятой"""
    global number_of_km
    global mkad_address
    many_addresses = ''
    # address = f'{mkad_address}'
    splitter = ','
    for number_of_km in range(0, number_of_mkad_s_kms + 1):
        many_addresses += f'{mkad_address} {number_of_km} kilometr vneshnayay storona{splitter}'
        # list_of_addresses_for_request.append(
        # f'{mkad_address} {number_of_km} kilometr vneshniaya storona')
        # number_of_km +=1
    # print(many_addresses.encode('utf-8'))
    # print(f'make_list_of_addresses_for_request: {list_of_addresses_for_request}')
    return many_addresses


def check_content():
    """Проверяет содержит ли файл координаты всех километров МКАД"""
    wb = load_workbook(f'./{excel_file}')  # открываем файл
    sheet = wb.active  # получаем текущий активный лист
    for col in sheet.iter_cols(min_col=1, max_col=2, min_row=2, max_row=number_of_mkad_s_kms + 2,
                               values_only=True):
        if 'POINT (' not in col and '0123456789.' not in col[7:-1]:
            return False
    return True


coords_of_Luhovitsy = Point(54.967192, 39.024195)


def create_geodataframe():
    """Возвращает geodataframe, содержащий координаты всех километров МКАД"""
    list_of_addresses = make_list_of_addresses_for_request().split(',')
    # Создаём GeoDataFrame, содержащий координаты всех километров МКАД
    coords_of_mkad_s_kms = geopandas.tools.geocode(list_of_addresses, provider='yandex',
                                                   api_key=API_KEY)

    return coords_of_mkad_s_kms


# print(longitude)
# plt.plot(longitude, latitude)
# plt.show()


def get_coords(ex_file):
    """Возвращает спсиок, содержащий вложенные списки с координатами каждого километра МКАД"""
    wb = load_workbook(ex_file)
    sheet_1 = wb.active
    for row in sheet_1.iter_rows(min_row=2, max_col=3, max_row=number_of_mkad_s_kms + 2, values_only=True):
        # получаем координаты точек для построения полигона МКАД
        coords = row[1].split('(')[-1].replace(')', '').split()
        coords = list(map(float, coords))
        # меняем местами координаты долготу с широтой, первая координата -  широта, вторая - долгота
        # для получения правильного результата с помощью функции geopy.distance.geodesic
        coords[0], coords[1] = coords[1], coords[0]
        # print(coords[0], coords[1])
        coords_for_polygon_mkad.append(coords)
    # print(coords_for_polygon_mkad)
    return coords_for_polygon_mkad


def read_ex_file():
    """Возвращает openpyxl.workbook.workbook.Workbook объект"""
    # file=excel_file
    # проверяем есть ли в текущей директории
    if excel_file not in os.listdir():
        # открываем файл,
        return get_coords(excel_file)
    # проверяем есть ли excel файл в текущей директории
    # elif excel_file not in os.listdir() or excel_file in os.listdir() and not check_content():
    #     # создаём файл, если его не было в текущей директории
    #     excel_file = create_geodataframe().to_excel(
    #     excel_writer='./coords_of_mkad_s_kms.xlsx')  # сохраняем координаты МКАД в файл

    # sheet= ex_file.active
    # return sheet


def show_graghic():
    latitude = []
    longitude = []
    km = 0
    for point in get_coords(excel_file):
        # print(f'point {km}: {point}')
        latitude.append(point[0])
        longitude.append(point[1])
        km += 1
    plt.plot(latitude, longitude)
    plt.show()


def find_distance(coords_of_Luhovitsy):
    """Возвращает расстояние от МКАД до адреса, введённого в поле формы 'адрес'"""
    # получаем координаты всех километров МКАД из файла
    coords = get_coords(excel_file)

    print(f'coords of mkad: {coords}')
    # создаём полигон из полученных координат
    poly_mkad = Polygon(coords)
    # находим точку на полигоне, ближайшую к точке, содержащей координаты адреса,
    # для которого требуется найти расстояние
    p1, nearest_pt = nearest_points(coords_of_Luhovitsy, poly_mkad)
    return geodesic((nearest_pt.x, nearest_pt.y), (coords_of_Luhovitsy.x, coords_of_Luhovitsy.y))


find_distance(coords_of_Luhovitsy)

# p.plot()
#
# show()
# poly_mkad = Polygon([[55.779747, 37.842555], [55.774527, 37.84313], [55.765483, 37.843157], [55.756447, 37.842681], [55.747546, 37.842223], [55.73888, 37.841576], [55.730101, 37.840516], [55.721072, 37.839402], [55.711671, 37.83721], [55.703053, 37.832602], [55.694353, 37.829503], [55.685391, 37.831335], [55.676605, 37.834731], [55.667879, 37.837911], [55.658363, 37.839663], [55.64984, 37.833985], [55.64347, 37.824418], [55.636656, 37.813989], [55.629867, 37.803595], [55.623397, 37.7934], [55.617358, 37.781775], [55.610799, 37.7699], [55.604824, 37.759048], [55.599265, 37.747532], [55.594016, 37.735], [55.588694, 37.722343], [55.583703, 37.709317], [55.578783, 37.696121], [55.573897, 37.682655], [55.571897, 37.665138], [55.57291, 37.648088], [55.57377, 37.63332], [55.574716, 37.617321], [55.575633, 37.601412], [55.577678, 37.58632], [55.581129, 37.57192], [55.584639, 37.557224], [55.588247, 37.542177], [55.591955, 37.526681], [55.595806, 37.512407], [55.602698, 37.501591], [55.610189, 37.492868], [55.617281, 37.484604], [55.624515, 37.476169], [55.631935, 37.467527], [55.639613, 37.458544], [55.647569, 37.449237], [55.654752, 37.440604], [55.661917, 37.432609], [55.670544, 37.425773], [55.67893, 37.419512], [55.687411, 37.414706], [55.695342, 37.407627], [55.702561, 37.397853], [55.709485, 37.388745], [55.718294, 37.383283], [55.727445, 37.378603], [55.736331, 37.374048], [55.745068, 37.369826], [55.754061, 37.368883], [55.762779, 37.369053], [55.771742, 37.369287], [55.780704, 37.36953], [55.790109, 37.373024], [55.797437, 37.380022], [55.805386, 37.38666], [55.814912, 37.390092], [55.823535, 37.392787], [55.832197, 37.395185], [55.841149, 37.394305], [55.850105, 37.392634], [55.858503, 37.397144], [55.866445, 37.404348], [55.872617, 37.415757], [55.877087, 37.429573], [55.881571, 37.444359], [55.882889, 37.459577], [55.885191, 37.474516], [55.889033, 37.489023], [55.894389, 37.501456], [55.900012, 37.514275], [55.905613, 37.528136], [55.907995, 37.544396], [55.90968, 37.560395], [55.911098, 37.575208], [55.909438, 37.590515], [55.905366, 37.605023], [55.901627, 37.619656], [55.898725, 37.634829], [55.896691, 37.650424], [55.895535, 37.666036], [55.89505, 37.682071], [55.894217, 37.697999], [55.889654, 37.711752], [55.883545, 37.723663], [55.877693, 37.735422], [55.871723, 37.747065], [55.865677, 37.758823], [55.859554, 37.770717], [55.853445, 37.782584], [55.84727, 37.794558], [55.841043, 37.806596], [55.834861, 37.818642], [55.828839, 37.830123], [55.8213, 37.837408], [55.812231, 37.839187], [55.802821, 37.840004], [55.793763, 37.841019], [55.785113, 37.841963]]

# print(poly_mkad)
# address_point, nearest_to_mkad = nearest_points(coords_of_Luhovitsy,
# poly_mkad)
# print(nearest_to_mkad)
# return address_point, nearest_to_mkad


# coords_of_Luhovitsy_longlat = geopy.Point(latitude=54.967192, longitude=39.024195)
# if excel_file not in os.listdir() or excel_file in os.listdir() and not check_content():
#     # Проверяем есть ли файл в директории и если файл есть, то проверяем содержит ли он
#     # координаты всех километров МКАД. Создаём файл если он отсутствует или не содержить координаты километров МКАД
#     create_exl_file()
# else:
#     print(open_exl_file())
# print(find_nearest_point(coords_of_Luhovitsy))
# print(get_coords(excel_file))
# print(find_nearest_point(coords_of_Luhovitsy))


# print(find_nearest_point(coords_of_Luhovitsy))

# array = [[37.842555, 55.779747], [37.84313, 55.774527], [37.843157, 55.765483], [37.842681, 55.756447], [37.842223, 55.747546], [37.841576, 55.73888], [37.840516, 55.730101], [37.839402, 55.721072], [37.83721, 55.711671], [37.832602, 55.703053], [37.829503, 55.694353], [37.831335, 55.685391], [37.834731, 55.676605], [37.837911, 55.667879], [37.839663, 55.658363], [37.833985, 55.64984], [37.824418, 55.64347], [37.813989, 55.636656], [37.803595, 55.629867], [37.7934, 55.623397], [37.781775, 55.617358], [37.7699, 55.610799], [37.759048, 55.604824], [37.747532, 55.599265], [37.735, 55.594016], [37.722343, 55.588694], [37.709317, 55.583703], [37.696121, 55.578783], [37.682655, 55.573897], [37.665138, 55.571897], [37.648088, 55.57291], [37.63332, 55.57377], [37.617321, 55.574716], [37.601412, 55.575633], [37.58632, 55.577678], [37.57192, 55.581129], [37.557224, 55.584639], [37.542177, 55.588247], [37.526681, 55.591955], [37.512407, 55.595806], [37.501591, 55.602698], [37.492868, 55.610189], [37.484604, 55.617281], [37.476169, 55.624515], [37.467527, 55.631935], [37.458544, 55.639613], [37.449237, 55.647569], [37.440604, 55.654752], [37.432609, 55.661917], [37.425773, 55.670544], [37.419512, 55.67893], [37.414706, 55.687411], [37.407627, 55.695342], [37.397853, 55.702561], [37.388745, 55.709485], [37.383283, 55.718294], [37.378603, 55.727445], [37.374048, 55.736331], [37.369826, 55.745068], [37.368883, 55.754061], [37.369053, 55.762779], [37.369287, 55.771742], [37.36953, 55.780704], [37.373024, 55.790109], [37.380022, 55.797437], [37.38666, 55.805386], [37.390092, 55.814912], [37.392787, 55.823535], [37.395185, 55.832197], [37.394305, 55.841149], [37.392634, 55.850105], [37.397144, 55.858503], [37.404348, 55.866445], [37.415757, 55.872617], [37.429573, 55.877087], [37.444359, 55.881571], [37.459577, 55.882889], [37.474516, 55.885191], [37.489023, 55.889033], [37.501456, 55.894389], [37.514275, 55.900012], [37.528136, 55.905613], [37.544396, 55.907995], [37.560395, 55.90968], [37.575208, 55.911098], [37.590515, 55.909438], [37.605023, 55.905366], [37.619656, 55.901627], [37.634829, 55.898725], [37.650424, 55.896691], [37.666036, 55.895535], [37.682071, 55.89505], [37.697999, 55.894217], [37.711752, 55.889654], [37.723663, 55.883545], [37.735422, 55.877693], [37.747065, 55.871723], [37.758823, 55.865677], [37.770717, 55.859554], [37.782584, 55.853445], [37.794558, 55.84727], [37.806596, 55.841043], [37.818642, 55.834861], [37.830123, 55.828839], [37.837408, 55.8213], [37.839187, 55.812231], [37.840004, 55.802821], [37.841019, 55.793763], [37.841963, 55.785113]]
# p1, nearest_to_mkad = nearest_points(coords_of_Luhovitsy,
#                                      poly_mkad)  # находим координаты точки на полигоне, которая находится ближе всего к точке, сродержащей координаты адреса, расстояние до которого требуется найти
# print(f'nearest_mkad_point.x: {nearest_to_mkad.x}, nearest_mkad_point.y: {nearest_to_mkad.y}')
# print(f'p1.x: {p1.x}, p1.y: {p1.y}')
# distance = geopy.distance.geodesic((coords_of_Luhovitsy.x, coords_of_Luhovitsy.y),
#                                    (nearest_to_mkad.x, nearest_to_mkad.y))
# print(f'distance from MKAD to Luhovitsy: {distance}')