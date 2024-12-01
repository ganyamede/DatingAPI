import geonamescache

gc = geonamescache.GeonamesCache()
cities = gc.get_cities()

def get_all_city(country_code):
    city_list = []
    for city_name, city_info in cities.items():
        if city_info['countrycode'] == country_code:
            city_list.append(city_info['name'])

    return city_list

def get_coordinates(city):
    for city_name, city_info in cities.items():
        if city_info['name'].lower() == city.lower() and city_info['countrycode'] == "UA":
            return city_info['latitude'], city_info['longitude']
    return None, None
#
# city = "Kyiv"
# latitude, longitude = get_coordinates(city)
#
# if latitude and longitude:
#     print(f"Координаты города {city}: Широта: {latitude}, Долгота: {longitude}")
# else:
#     print(f"Город {city} не найден в базе данных.")
