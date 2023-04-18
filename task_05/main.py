from PIL import Image
import random

color = (255, 255, 255)
steps = 10

def get_cell_status(living_cell_possibility):
    if random.random() > living_cell_possibility:
        return False
    else:
        return True

def check_neighbours(x, y, width, hight, img):
    living_neighbours = 0
    x_neighbours = [-1, 0, 1]
    y_neighbours = [-1, 0, 1]
    if x == width - 1:
        x_neighbours.pop(2)
    if x == 0:
        x_neighbours.pop(0)
    if y == hight - 1:
        y_neighbours.pop(2)
    if y == 0:
        y_neighbours.pop(0)
    for x_n in x_neighbours:
        for y_n in y_neighbours:
            if x_n == 0 and y_n == 0:
                continue
            if img.getpixel((x + x_n, y + y_n)) == color:
                living_neighbours += 1
    return living_neighbours

def step(prev_img, width, hight):
    next_img = Image.new("RGB", (width, hight), (0,0,0))
    for x in range(width):
        for y in range(hight):
            curent_pixel = prev_img.getpixel((x, y))
            living_neighbours = check_neighbours(x, y, width, hight, prev_img)
            was_alive = True if curent_pixel == color else False
            is_alive = False
            if not was_alive and living_neighbours == 3:
                is_alive = True
            elif was_alive and (living_neighbours == 2 or living_neighbours == 3):
                is_alive = True
            if is_alive:
                next_img.putpixel((x,y), color)
            else:
                r = int(max(curent_pixel[0] - color[0]/steps, 0))
                g = int(max(curent_pixel[1] - color[1]/steps, 0))
                b = int(max(curent_pixel[2] - color[2]/steps, 0))
                next_img.putpixel((x,y), (r, g, b))
    return next_img

def set_color():
    print('Input color (R, G, B):')
    r = int(input('Input red   (0 - 255) >>> '))
    g = int(input('Input green (0 - 255) >>> '))
    b = int(input('Input blue  (0 - 255) >>> '))
    global color
    color = (r, g, b)
    menu()

def generate_initial_plane():
    width = int(input('Input image width in pixels >>> '))
    height = int(input('Input image height in pixels >>> '))
    density = float(input('Input living cells dencity (0 to 1) >>> '))
    name = input('Input image name with format >>> ')
    img = Image.new("RGB", (width, height), (0,0,0))
    for x in range(width):
        for y in range(height):
            if get_cell_status(density):
                img.putpixel((x,y), color)
    img.save(name)
    menu()

def set_steps():
    global steps
    steps = int(input('Input number of steps >>> '))
    menu()

def game():
    name = input('Input image name with format >>> ')
    cur_img = Image.open(name)
    width, hight = cur_img.size
    for i in range(steps):
        print('Step ' + str(i) + ' in progress...')
        cur_img = step(cur_img, width, hight)
    cur_img.save('GameOfLIfe-'+ str(i) +'Steps.png')
    print('DONE!')
    menu()


def start():
    print('''
###################################
##### WELCOME TO GAME OF LIFE #####
###################################''')
    menu()

def menu():
    print(f'''
Commands:
'color' - set color for alive cells
'gen'   - generate initial field
'steps' - number of game steps
'play'  - start game of life
'end'   - close programm
-----------------------------------
Current color: {color}
Current steps: {steps}
-----------------------------------
''')
    command = input('Input comand >>> ')
    if command.casefold() == 'color':
        set_color()
    elif command.casefold() == 'gen':
        generate_initial_plane()
    elif command.casefold() == 'steps':
        set_steps()
    elif command.casefold() == 'play':
        game()
    elif command.casefold() == 'end':
        print('Done')
    else:
        print('Invalid command, ignoring')
        menu()

if __name__ == '__main__':
    start()