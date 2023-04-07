import math

def input_data():
    return {
        "d1": float(input('Введите кратчайшее расстояние между спасателем и кромкой воды, d1 (ярды) => ')),
        "d2": float(input('Введите кратчайшее расстояние от утопающего до берега, d2 (футы) => ')),
        "h": float(input('Введите боковое смещение между спасателем и утопающим, h (ярды) => ')),
        "v_sand": float(input('Введите скорость движения спасателя по песку, v_sand (мили в час) => ')),
        "n": float(input('Введите коэффициент замедления спасателя при движении в воде, n => ')),
        }

def calculate_time(d1, d2, h, v_sand, n, theta1):
    # Convert to feet
    d1 *= 3
    h *= 3

    # Calculations
    x = d1 * math.tan(math.radians(theta1))
    l1 = math.sqrt(x ** 2 + d1 ** 2)
    l2 = math.sqrt((h - x) ** 2 + d2 ** 2)
    t = ((l1 + n * l2) / 5280) / v_sand # result in hours

    # Convert to seconds
    t *= 60 * 60
    return t

def calculate_optimal_angle(d1, d2, h, v_sand, n):
    best_time = None
    best_angle = None
    # Iterate through possible angles to find the optimal one
    for theta1 in range(0, 90, 1):
        time = calculate_time(d1, d2, h, v_sand, n, theta1)
        if best_time is None or time < best_time:
            best_time = time
            best_angle = theta1
    return best_time, best_angle

def lifeguard_problem():
    data = input_data()
    time, theta1 = calculate_optimal_angle(data['d1'], data['d2'], data['h'], data['v_sand'], data['n'])

    # Display result
    print("Если спасатель начнёт движение под углом theta1, равным {:.0f} градусам, он достигнет утопащего через {:.1f} секунды".format(theta1, time))

if __name__ == "__main__":
    lifeguard_problem()