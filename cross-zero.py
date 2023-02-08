from colorama import Fore, Back, Style

field_size = 3  # Размер поля
clear_field = '-'  # Обозначение пустых ячеек поля
field = [[clear_field for j in range(field_size)] for i in range(field_size)]  # Создание поля
columns = [["   "] + [str(j) + " " for j in range(field_size)]]  # Обозначение столбцов


# user1 = 'O'
# user2 = 'X'


#  Определяем кто будет ходить первым
def who_first(user1='O', user2='X'):
    while True:
        xo = input(Style.BRIGHT + "Кретиком или Ноликом будете начинать игру? " + Style.RESET_ALL)

        if len(xo) != 1:
            print(Style.BRIGHT + Fore.RED, "Введите один символ Х или О: ", Style.RESET_ALL)
        if (xo.upper() != 'X' and xo.upper() != chr(1093).upper()) and (
                xo.upper() != 'O' and xo.upper() != chr(1086).upper()):
            print(Style.BRIGHT + Fore.RED + "Введите Х или О: ", Style.RESET_ALL)
            continue
        if xo.upper() == 'X':
            user1 = 'X'
            user2 = 'O'
            break
        break
    return user1, user2


# Отображение поля с координатами
def show_field(f):
    for i in range(0, len(columns)):
        print(*columns[i], " ")

    for i in range(0, len(f)):
        print(str(i), " ", end="")
        for j in range(0, len(f[i])):
            if f[i][j] == 'X':
                print(Back.LIGHTWHITE_EX + Fore.RED + Style.BRIGHT, f[i][j], Style.RESET_ALL, end="")
            if f[i][j] == 'O':
                print(Back.LIGHTWHITE_EX + Fore.GREEN + Style.BRIGHT, f[i][j], Style.RESET_ALL, end="")
            if f[i][j] == clear_field:
                print(Back.LIGHTWHITE_EX + Fore.LIGHTBLACK_EX + Style.DIM, f[i][j], Style.RESET_ALL, end="")
        print()
    print()


def entering_coordinates(f, user):
    while True:
        coordinates = input(
            Style.BRIGHT + f"Ход {user}. Введите две координаты," \
                           " через пробел (№строки №столбца): " + Style.RESET_ALL).split()
        if len(coordinates) != 2:
            print(
                Style.BRIGHT, Fore.RED, "Введите две координаты, через пробел: ", Style.RESET_ALL)
            continue
        if not (coordinates[0].isdigit() and coordinates[1].isdigit()):
            print(Style.BRIGHT, "Введите числа: ", Style.NORMAL)
            continue
        scale = [i for i in range(0, field_size)]
        x = int(coordinates[0])
        y = int(coordinates[1])
        if not (x in scale and y in scale):
            print(
                Style.BRIGHT + Fore.RED + "Введенные координаты"\
                                          f" за пределом поля {field_size}X{field_size}: ", Style.RESET_ALL)
            continue
        if f[x][y] != '-':
            print(Style.BRIGHT + Fore.RED + "Клетка занята" + Style.RESET_ALL)
            continue
        break
    return x, y


def win_combo(f, user):
    f_list = []
    for n in f:
        f_list += n
    positions = [[0, 1, 2], [3, 4, 5], [6, 7, 8], [0, 3, 6], [1, 4, 7], [2, 5, 8], [0, 4, 8], [2, 4, 6]]
    indices = set([i for i, j in enumerate(f_list) if j == user])

    for p in positions:
        if len(indices.intersection(set(p))) == 3:
            return True
    return False


motion = 1
user1, user2 = who_first()
while True:

    if motion % 2 == 0:
        mark = user2  # 'X'
    else:
        mark = user1  # 'O'
    show_field(field)
    x, y = entering_coordinates(field, mark)
    field[x][y] = mark
    if motion == field_size ** 2:
        print(Style.BRIGHT, Fore.BLUE, "Ничья", Style.RESET_ALL)
        break
    if win_combo(field, mark):
        print(Style.BRIGHT, Fore.GREEN, f"Выйграл {mark}", Style.RESET_ALL)
        show_field(field)
        break
    motion += 1
