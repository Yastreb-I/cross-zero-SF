from colorama import Fore, Back, Style


#  field_size = 7  # Размер поля
#  max_sequence = 4  # Длина выйгрышной комбинации


# user1 = 'O'
# user2 = 'X'

#  Параметры игры
def parametri_game(field_size=3, max_sequence=3):
    print(Style.BRIGHT, Fore.CYAN, "Добро пожаловать в игру крестики-нолики!", Style.RESET_ALL)
    while True:
        field_size = input(Style.BRIGHT + "Введите число, которое будет означать "
                                          "количество строк и столбцов для поля: " + Style.RESET_ALL)
        if not field_size.isdigit():
            print(Style.BRIGHT + Fore.RED, "Введите только число: ", Style.RESET_ALL)
            continue
        if int(field_size) < 3:
            print(Style.BRIGHT + Fore.RED, "Введите число большее или равное 3: ", Style.RESET_ALL)
            continue
        max_sequence = input(
            Style.BRIGHT + "Введите одно число, которое будет означать серию символов по вертикали, горизонтали или "
                           "диагонали для выигрыша: " + Style.RESET_ALL)
        if not max_sequence.isdigit():
            print(Style.BRIGHT + Fore.RED, "Введите только число: ", Style.RESET_ALL)
            continue
        if int(max_sequence) < 3:
            print(Style.BRIGHT + Fore.RED, "Введите большее или равное 3: ", Style.RESET_ALL)
            continue
        if int(max_sequence) > int(field_size):
            print(Style.BRIGHT + Fore.RED, "Длина выигрышного рядя не может быть длиннее размера поля!",
                  Style.RESET_ALL)
            continue
        break
    return int(field_size), int(max_sequence)


field_size, max_sequence = parametri_game()
clear_field = '-'  # Обозначение пустых ячеек поля
field = [[clear_field for j in range(field_size)] for i in range(field_size)]  # Создание поля
columns = [["   "] + [str(j) + " " for j in range(field_size)]]  # Обозначение столбцов


#  Определяем кто будет ходить первым
def who_first(user1='O', user2='X'):
    while True:
        xo = input(Style.BRIGHT + "Кретиком или Ноликом будете начинать игру? " + Style.RESET_ALL)

        if len(xo) != 1:
            print(Style.BRIGHT + Fore.RED, "Введите один символ Х или О: ", Style.RESET_ALL)
        if (xo.upper() != 'X' and xo.upper() != chr(1093).upper()) and (
                xo.upper() != 'O' and xo.upper() != chr(1086).upper()) and xo.upper() != '0':
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
    # print()


# Проверка введенных координат от игроков
def entering_coordinates(f, user):
    while True:
        coordinates = input(
            Style.BRIGHT + "Ход " + Fore.CYAN + f"{user}" + Fore.RESET + ". Введите две координаты,"
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
                Style.BRIGHT + Fore.RED + "Введенные координаты" \
                                          f" за пределом поля {field_size}X{field_size}: ", Style.RESET_ALL)
            continue
        if f[x][y] != '-':
            print(Style.BRIGHT + Fore.RED + "Клетка занята" + Style.RESET_ALL)
            continue
        break
    return x, y


def win_combo(f, user):
    wincombo = user * max_sequence
    #  Поиск выигрышной комбинации по строке (горизонтали)
    for r in range(0, len(f)):
        combo_row = "".join(f[r])
        if combo_row.find(wincombo) != -1:
            return True
        #  Поиск выигрышной комбинации по столбцу (вертикали)
        combo_col = ""
        for c in range(0, len(f[r])):
            combo_col = combo_col + f[c][r]
            if combo_col.find(wincombo) != -1:
                return True

    #  Поиск выигрышной комбинации по диагонали сверху вниз
    combo_diag_r = ""
    combo_diag_l = ""
    for row in range(-1 * field_size + len(wincombo), field_size + 1 - len(wincombo), 1):

        position_l = [rdl for rdl in range(row, row + field_size, 1)]

        position_c = [c for c in range(0, field_size)]
        for diag in range(0, field_size):
            xl = position_l[diag]
            yl = position_c[diag]
            if 0 <= xl <= field_size - 1:
                combo_diag_l = combo_diag_l + f[xl][yl]
        if combo_diag_l.find(wincombo) != -1:
            return True
    #  Поиск выигрышной комбинации по диагонали снизу в верх
    for ro in range(2 * field_size - len(wincombo), field_size - len(wincombo), -1):

        position_r = [rdr for rdr in range(ro, ro - field_size, -1)]

        position_c = [c for c in range(0, field_size)]
        for diag in range(0, field_size):
            xr = position_r[diag]
            yr = position_c[diag]
            if 0 <= xr <= field_size - 1:
                combo_diag_r = combo_diag_r + f[xr][yr]
        if combo_diag_r.find(wincombo) != -1:
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
        show_field(field)
        print(Style.BRIGHT, Fore.GREEN, f"Выйграл {mark}", Style.RESET_ALL)
        break

    motion += 1
