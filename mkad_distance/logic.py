import os
from typing import List, Union
import geopandas
from geopandas import GeoDataFrame
from geopy.distance import geodesic
from geopy.geocoders import Yandex
from loguru import logger
from shapely.geometry import Polygon, Point
from shapely.ops import nearest_points

API_KEY = 'cbddbd2c-95ce-4aa1-ba5a-5d0416597c20'
ya_geocoder: Yandex = Yandex(api_key=API_KEY)  # геокодер, используемый для геокодирования адреса
mkad_s_kms: int = 108  # кол-во километров МКАД
mkad_address: str = 'Россия Москва МКАД'  # неизменяющееся часть адреса МКАД, используемая для формирования адреса
# каждого км МКАД
coords_mkad: list = []
shape_file = 'dataframe.shp'
list_mkad_s_km: List[float] = []  # список, для хранения координат каждого километра МКАД


def make_list_of_addresses_for_request():
    """Возвращает строку, содержащую адреса всех километров МКАД, разделённых запятой"""
    many_addresses = ''
    splitter = ','
    for number_km in range(0, mkad_s_kms + 1):
        many_addresses += f'{mkad_address} {number_km} kilometr vneshnayay storona{splitter}'
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


def get_blprt_root() -> str:
    """Возвращает путь до директории "mkad_distance" """
    from .blueprint import mkad_distance
    return mkad_distance.root_path


def check_file(path: str) -> None:
    """Проверяет есть ли .shp файл в директории 'path' """
    # path_shp: str = f'{get_blprt_root()}/data'
    # path_shp: str = f'{os.getcwd()}/data'
    # if shape_file in os.listdir(dir_to_file):
    if shape_file in os.listdir(path):
        # если .shp файл, есть ничего не делаем
        pass

    elif shape_file not in os.listdir(path):
        # создаём .shp файл, если его не было в текущей директории и сохраняем в него координаты всех километров МКАД
        create_geodataframe().to_file(shape_file)


def get_polygon(shp_file: str, path) -> Polygon:
    """Возвращает полигон, содержащий координаты точек каждого километра МКАД"""
    # blueprint_path = get_blprt_root()
    # blueprint_path = os.getcwd()
    gdf: GeoDataFrame = geopandas.read_file(f'{path}/{shp_file}')
    coords = make_lan_lon_coords(gdf)
    poly_mkad = Polygon(coords)
    return poly_mkad


def write_in_log(address: str, distance: float, path) -> None:
    """Записывает результат расчёта в .log файл"""
    path: str = f'{path}/info.log'  # путь до .log файла
    logger.add(path, format='{time} {message}', level='INFO')
    logger.info(f'Расстояние: МКАД - {address} равно {distance}')


def find_distance(coords_of_address: Point, polygon: Polygon) -> Union[float, int]:
    """Возвращает расстояние в километрах от МКАД до адреса, введённого в поле формы 'адрес'"""
    # ищем точку (nearest_pt) на МКАД,
    # расположенную ближе всего к
    # точке, с координатами адреса, расстояние до которого (адреса) требуется найти
    p1, nearest_pt = nearest_points(coords_of_address, polygon)
    distance = geodesic((nearest_pt.x, nearest_pt.y), (coords_of_address.x, coords_of_address.y))
    if distance.km % 1 == 0:
        return int(distance.km)
    return round(distance.km, 1)
