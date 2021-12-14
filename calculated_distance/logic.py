import os
from typing import List, Union, Dict
from geopandas import GeoDataFrame
import geopandas
from geopy import Location
from loguru import logger
from geopy.geocoders import Yandex
from shapely.geometry import Polygon, Point
from shapely.ops import nearest_points
from geopy.distance import geodesic


API_KEY = 'cbddbd2c-95ce-4aa1-ba5a-5d0416597c20'
ya_geocoder: Yandex = Yandex(api_key=API_KEY)  # геокодер, используемый для геокодирования адреса
number_of_mkad_s_kms: int = 108  # кол-во километров МКАД
mkad_address: str = 'Россия Москва МКАД'  # неизменяющееся часть адреса МКАД, используемая для формирования адреса
# каждого км МКАД
number_of_km: int = 0  # номер километра МКАД, начиная с нулевого
coords_mkad: list = []
url: str = f'https://geocode-maps.yandex.ru/1.x/'
blueprint: str = 'calculated_distance'
shape_file = 'dataframe.shp'
list_mkad_s_km: List[float] = []  # список, для хранения координат каждого километра МКАД
dir_to_shape_file: str = os.getcwd() + '/' + blueprint
#dir_to_shape_file: str = os.getcwd()


def make_list_of_addresses_for_request():
    """Возвращает строку, содержащую адреса всех километров МКАД, разделённых запятой"""
    many_addresses = ''
    splitter = ','
    for number_of_km in range(0, number_of_mkad_s_kms + 1):
        many_addresses += f'{mkad_address} {number_of_km} kilometr vneshnayay storona{splitter}'
    return many_addresses


def create_geodataframe() -> GeoDataFrame:
    """Возвращает GeoDataFrame, содержащий координаты всех километров МКАД"""
    list_of_addresses = make_list_of_addresses_for_request().split(',')
    # Создаём GeoDataFrame, содержащий координаты всех километров МКАД
    coords_of_mkad_s_kms = geopandas.tools.geocode(list_of_addresses, provider='yandex',
                                                   api_key=API_KEY)
    return coords_of_mkad_s_kms


def make_lan_lon_coords(gdf: GeoDataFrame) -> List[Point]:
    global list_mkad_s_km
    for point in gdf.geometry:
        if isinstance(point, Point):
            list_mkad_s_km.append(point.y)  # Добавляем первую координату - широту
            list_mkad_s_km.append(point.x)  # Добавляем первую координату - долготу
            pt: Point = Point(list_mkad_s_km)
            coords_mkad.append(pt)  # Добавляем точку Point в список, содержащий координаты точек всех километров МКАД
            list_mkad_s_km = []  # Очищаем список для последующих итераций
        elif not isinstance(point, Point):
            continue
    return coords_mkad


def check_file():
    """Проверяет есть ли .shp файл в директории <calculated_distance>"""
    # проверяем есть ли файл .shp в текущей директории
    if shape_file in os.listdir(dir_to_shape_file):
        # усли есть ничего не делаем
        pass

    elif shape_file not in os.listdir('.') or shape_file in os.listdir('.'):
        # создаём .shp файл, если его не было в текущей директории и сохраняем в него координаты всех километров МКАД
        create_geodataframe().to_file(shape_file)


def get_polygon(shape_file: str) -> Polygon:
    """Возвращает полигон, содержащий координаты точек каждого километра МКАД"""
    gdf = geopandas.read_file(dir_to_shape_file + '/' + shape_file)
    coords = make_lan_lon_coords(gdf)
    poly_mkad = Polygon(coords)
    return poly_mkad


def get_location(address: str) -> Location:
    """Возвращает кортеж, содержащий широту и долготу"""
    location: Location = ya_geocoder.geocode(address)
    return location


def write_in_log(address: str, distance: float):
    path = f'{os.getcwd()}/{blueprint}/info.log'
    logger.add(path, format='{time} {message}', level='INFO')
    logger.info(f'Расстояние от МКАД до {address} равно {distance} км')


def find_distance(coords_of_address) -> Union[int, float]:
    """Возвращает расстояние в километрах от МКАД до адреса, введённого в поле формы 'адрес'"""
    # получаем координаты всех километров МКАД из .xlsx файла
    check_file()
    poly_mkad = get_polygon(shape_file)
    print(f'find_distance: {poly_mkad.contains(coords_of_address)}')
    if poly_mkad.contains(coords_of_address):
        return 0
    # находим точку на полигоне, ближайшую к точке, содержащей координаты адреса <coords_of_address>,
    # для которого требуется найти расстояние
    else:
        # ищем точку (nearest_pt) на МКАД,
        # расположенную ближе всего к
        # точке, с координатами адреса, расстояние до которого требуется найти
        p1, nearest_pt = nearest_points(coords_of_address, poly_mkad)
        print(f'nearest_pt: {nearest_pt}')
        distance = geodesic((nearest_pt.x, nearest_pt.y), (coords_of_address.x, coords_of_address.y))
        return round(distance.km, 1)


def get_toponims(address: str) -> List[str]:
    """Возвращает список словарей, содержащих виды топонимов и значения этих топонимов"""
    list_toponims = []
    location: Location = ya_geocoder.geocode(address)
    toponims_type: List[dict] = location.raw['metaDataProperty']['GeocoderMetaData']['Address']['Components']
    for item in toponims_type:
        list_toponims.append(item['kind'])
        list_toponims.append(item['name'])
    return list_toponims



