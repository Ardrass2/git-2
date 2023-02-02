import sys
from geocoder import get_coordinates, get_ll_span
from mapapi_PG import show_map
from distance import lonlat_distance
from business import find_business


def main():
    toponym_to_find = " ".join(sys.argv[1:])
    lat, lon = get_coordinates(toponym_to_find)
    address_ll = f"{lat},{lon}"
    span = f"0.005,0.005"
    org = find_business(address_ll, span, 'аптека')
    point = org['geometry']['coordinates']
    org_lat = float(point[0])
    org_lon = float(point[1])
    point_params = f'pt={org_lat},{org_lon},pm2dgl'

    show_map(f"ll={address_ll}&spn={span}", "map", add_params=point_params)

    point_params = point_params + f"~{address_ll},pm2rdl"
    show_map(f"ll={address_ll}&spn={span}", "map", add_params=point_params)

    show_map(map_type="map", add_params=point_params)
    name = org['properties']['CompanyMetaData']['name']
    address = org['properties']['CompanyMetaData']['address']
    time = org['properties']['CompanyMetaData']['Hours']['text']
    dist = lonlat_distance((lon, lat), (org_lon, org_lat))

    snippet = f"Название:\t{name}\n" \
              f"Адрес: \t\t{address}\n" \
              f"Время работы:\t{time}\n" \
              f"Расстояние:\t{dist} м\t"
    print(snippet)


if __name__ == "__main__":
    main()