import zip_util
import math
zip_codes = zip_util.read_zip_all()

def format_coords(lat, lon):
    lat_dms = (abs(lat), math.floor(abs(lat)) , (abs(lat) - math.floor(abs(lat))) * 60)
    lon_dms = (abs(lon), math.floor(abs(lon)) , (abs(lon) - math.floor(abs(lon))) * 60)
    lat_str = "{:03d}\u00b0{:02d}'{:05.2f}\"{}".format(int(lat_dms[1]), int(lat_dms[2]), (lat_dms[2] - int(lat_dms[2])) * 60, "N" if lat >= 0 else "S")
    lon_str = "{:03d}\u00b0{:02d}'{:05.2f}\"{}".format(int(lon_dms[1]), int(lon_dms[2]), (lon_dms[2] - int(lon_dms[2])) * 60, "E" if lon >= 0 else "W")
    return lat_str + "," + lon_str

def haversine(coord1, coord2):
    lat1, lon1 = coord1
    lat2, lon2 = coord2
    lat1, lon1, lat2, lon2 = map(math.radians, [lat1, lon1, lat2, lon2])
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = math.sin(dlat / 2) ** 2 + math.cos(lat1) * math.cos(lat2) * math.sin(dlon / 2) ** 2
    c = 2 * math.asin(math.sqrt(a))
    r = 3956
    distance = c * r
    return distance

def find_location():
    zip = int(input("Enter a ZIP Code to lookup => "))
    data = None
    for z in zip_codes:
        if int(z[0]) == zip:
            data = z
    if data:
        print(f'ZIP Code {data[0]} is in {data[3]}, {data[4]}, {data[5]} county,')
        print(f'coordinates: ({format_coords(data[1], data[2])})')
    else:
        print('ZIP not found, try again')
    menu()

def find_zip():
    city = input("Enter a city name to lookup => ")
    state = input("Enter the state name to lookup => ")
    data = []
    for z in zip_codes:
        if city.casefold() == z[3].casefold() and state.casefold() == z[4].casefold():
            city = z[3]
            state = z[4]
            data.append(int(z[0]))
    if len(data):
        print(f'The following ZIP Code(s) found for {city}, {state}: {str(data)[1:-1]}')
    else:
        print('The city was not found, try again')
    menu()

def measure_dist():
    zip1 = int(input("Enter the first ZIP Code => "))
    zip2 = int(input("Enter the second ZIP Code => "))
    data = []
    for z in zip_codes:
        if int(z[0]) == zip1 or int(z[0]) == zip2:
            data.append([z[1], z[2]])
    if len(data) == 2:
        print(f'The distance between {str(zip1)} and {str(zip2)} is {round(haversine(data[0], data[1]), 2)} miles')
    else:
        print('One ore both ZIP codes were not found, try again')
    menu()

def start():
    print('''
#################################
##### WELCOME TO ZIP FINDER #####
#################################
''')
    menu()

def menu():
    command = input("Command ('loc', 'zip', 'dist', 'end') => ")
    if command.casefold() == 'loc':
        find_location()
    elif command.casefold() == 'zip':
        find_zip()
    elif command.casefold() == 'dist':
        measure_dist()
    elif command.casefold() == 'end':
        print('Done')
    else:
        print('Invalid command, ignoring')
        menu()

if __name__ == '__main__':
    start()