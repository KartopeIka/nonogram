import tkinter as tk
import random
import numpy as np

# Використані кольори
white = "#F5F5F5"
black_and_white = ["0", "#000000"]
mistakes_count = 0
changes_permission = True
win = False
colour_count = 0


# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=-=-ANSWERS=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# функція для зчитування заготовленої матриці відповідей з файлу
def answers_from_file(file_name):
    answers = []
    answers_file = open(file_name, "r")
    for line in answers_file:
        line_answers = []
        for unit in line.split():
            line_answers.append(unit)
        answers.append(line_answers)
    answers_file.close()
    return answers

# генерування випадкової матриці відповідей
def random_answers(rows,cols):
    return [[random.choice(black_and_white) for _ in range(cols)] for _ in range(rows)]


# максимальна кількість чисел збоку
def numbers_amount(size):
    if size % 2:
        return size // 2+1
    return size // 2

# Заповнення списків допоміжних чисел збоку
def numbers_search(rows, cols, answers):
    numbers = [[] for _ in range(rows)]
    for row in range(rows):
        count = 0
        for col in range(cols):
            if answers[row][col] != '0':
                count += 1
            elif count:
                numbers[row].append(count)
                count = 0
        if count:
            numbers[row].append(count)
    return numbers

# Рахуємо скільки клітинок має бути заповнено для перемоги
def win_count_search(rows, cols, answers):
    global colour_count
    colour_count = 0
    win_count = 0
    for row in range(rows):
        for col in range(cols):
            if answers[row][col] != '0':
                win_count +=1
    return win_count

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-CLICK=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# Клас для елементів основного ігрового поля
class Nonobutton:
    def __init__(self, colour, button_grid, pixel):
        self.button = tk.Button(button_grid, relief='groove', bg=white,
                                image=pixel, height=50, width=50)
        self.colour = colour
        self.status = "no"

# ліва кнопка миші відповідає за розфарбовування клітинок
def left_click(button: Nonobutton, win_count, nonogram, mistakes, red_x_image):
    global changes_permission
    # Якщо клітинка "не татиснута" та дозволено вносити зміни до ігрового поля
    if button.status == "no" and changes_permission:
        # Якщо клітинка є частиною відповіді нонограми
        if button.colour != '0':
            # Змінюємо її колір
            button.button.configure(bg=button.colour)
            button.status = "color"
            # Збільшуємо кількість розфарбованих клітинок
            global colour_count
            colour_count+=1
            # Перевіряємо чи вже переміг користувач
            if colour_count == win_count:
                # забороняємо подальше внесення змін до поля
                changes_permission = False
                # виводимо повідомлення про виграш
                win_label = tk.Label(nonogram, text="You won!", font=('Arial', 18))
                win_label.place(relx=0.5, rely=0.6, anchor="center")
        # Інакше користувач помилився
        else:
            # Додаємо до клітинки позначку помилки
            button.button.configure(image=red_x_image)
            button.status = "wrong"
            # Оновлюємо лічильник помилок
            global mistakes_count
            mistakes_count += 1
            mistakes.configure(text=f"Mistakes: {mistakes_count}")

# права кнопка миші відповідає за встановлення допоміжних позначок
def right_click(button: Nonobutton, gray_x_image, pixel):
    # Якщо дозволено вносити зміни до ігрового поля
    if changes_permission:
        # Якщо клітинка "не натиснута"
        if button.status == "no":
            # Додаємо до неї картинку допоміжної позначки
            button.button.configure(image=gray_x_image)
            button.status = "x"
        # Якщо клітинка вже містить допоміжну позначку
        elif button.status == "x":
            # Прибираємо її
            button.button.configure(image=pixel)
            button.status = "no"



# перезапуск програми з новою матрицею відповідей
def refresh(nonogram_window, answers: list):
    nonogram_window.destroy()
    global changes_permission
    changes_permission = True
    create_nonogram(answers)

# -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=ОСНОВНА ФУНКЦІЯ=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
# основна функція приймає на вхід матрицю відповідей
def create_nonogram(answers):
    # вікно програми
    nonogram = tk.Tk()
    nonogram.title("Nonogram")

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=МЕНЮ=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # створення усіх гілок меню, та призначення їм дій
    main_menu = tk.Menu(nonogram)

    # -=-=-=-=-=PRE MADE=-=-=-=-=-=-
    # Заготовлені кросворди
    pre_made_menu = tk.Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label="Pre made", menu=pre_made_menu)
    # Кольорові заготовки
    pre_made_colour_menu = tk.Menu(main_menu, tearoff=False)
    pre_made_menu.add_cascade(label="colour", menu = pre_made_colour_menu)
    # Варіанти кольорових заготовок
    pre_made_colour_menu.add_command(label="4x4", command=lambda: refresh(nonogram, answers_from_file("test2.txt")))
    pre_made_colour_menu.add_command(label="5x5", command=lambda: refresh(nonogram, answers_from_file("test.txt")))
    pre_made_colour_menu.add_command(label="8x10", command=lambda: refresh(nonogram, answers_from_file("8x10_colour.txt")))
    pre_made_colour_menu.add_command(label="10x10", command=lambda: refresh(nonogram, answers_from_file("10x10_colour.txt")))
    # Ч/Б заготовки
    pre_made_bw_menu = tk.Menu(main_menu, tearoff=False)
    pre_made_menu.add_cascade(label="black/white", menu = pre_made_bw_menu)
    # Варіанти Ч/Б заготовок
    pre_made_bw_menu.add_command(label="10x10", command=lambda: refresh(nonogram, answers_from_file("10x10_bw")))
    pre_made_bw_menu.add_command(label="11x9", command=lambda: refresh(nonogram, answers_from_file("11x9_bw")))

    # -=-=-=-=-=RANDOM=-=-=-=-=-=-
    # Кросворди з випадковими відповідями
    random_menu = tk.Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label="Random", menu=random_menu)
    # Різні розміри
    random_menu.add_command(label="4x4", command=lambda: refresh(nonogram, random_answers(4,4)))
    random_menu.add_command(label="5x5", command=lambda: refresh(nonogram, random_answers(5,5)))
    random_menu.add_command(label="6x6", command=lambda: refresh(nonogram, random_answers(6,6)))
    random_menu.add_command(label="7x7", command=lambda: refresh(nonogram, random_answers(7,7)))

    nonogram.configure(menu=main_menu)


    # Запис кількості помилок
    global mistakes_count
    mistakes_count = 0
    mistakes = tk.Label(nonogram, text=f"Mistakes: {mistakes_count}", font=('Arial', 18))
    mistakes.pack(padx=20, pady=20)


    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=VARIABLES=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # обраховуємо розміри основного ігрового поля
    rows = len(answers)
    cols = len(answers[0])
    # максимально можлива кількість чисел збоку ігрового поля
    rows_numbers_amount = numbers_amount(rows)
    cols_numbers_amount = numbers_amount(cols)
    # кількість клітинок, які має заповнити користувач для перемоги
    win_count = win_count_search(rows, cols, answers)

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=КАРТИНКИ=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # Даний файл необхідний для задання розмірів сітки у пікселях
    pixel = tk.PhotoImage(width=1, height=1)
    # допоміжна позначка
    gray_x_image = tk.PhotoImage(file=r"green_cat_x.png")
    # помилка
    red_x_image = tk.PhotoImage(file=r"red_cat_x.png")

    # -=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=СІТКА=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-
    # ініціалізація сітки для розміщення елементів
    button_grid = tk.Frame(nonogram)
    for row in range(rows + rows_numbers_amount):
        button_grid.rowconfigure(row, weight=1)
    for col in range(cols + cols_numbers_amount):
        button_grid.columnconfigure(col, weight=1)

    # Створюємо елементи основного поля
    nonobuttons = [[Nonobutton(answers[row][col], button_grid, pixel) for col in range(cols)] for row in range(rows)]
    # Списки чисел збоку
    rows_numbers = numbers_search(rows, cols, answers)
    cols_numbers = numbers_search(cols, rows, np.array(answers).transpose())


    # додаємо до сітки записи вгорі та зліва
    for row in range(rows):
        for col in range(len(rows_numbers[row])):
            number = tk.Label(button_grid, text=f"{rows_numbers[row][col]}")
            number.grid(row=row + rows_numbers_amount, column=col)

    for col in range(cols):
        for row in range(len(cols_numbers[col])):
            number = tk.Label(button_grid, text=f"{cols_numbers[col][row]}")
            number.grid(row=row, column=col + cols_numbers_amount)

    # додаємо до сітки записи клітинки ігрового поля
    for row in range(rows):
        for col in range(cols):
            # Призначаємо кнопкам функції, які виконуються при натиску на ліву кнопку миші
            nonobuttons[row][col].button.bind("<Button-1>", lambda e, button=nonobuttons[row][col]: left_click(button,win_count,nonogram,mistakes,red_x_image))
            # та на праву кнопку миші
            nonobuttons[row][col].button.bind("<Button-3>", lambda e, button=nonobuttons[row][col]: right_click(button, gray_x_image, pixel))
            # Додаємо елементи до сітки
            nonobuttons[row][col].button.grid(row=row + rows_numbers_amount, column=col + cols_numbers_amount,
                                              sticky=tk.W + tk.E)
    button_grid.pack(padx=20, pady = 20)


    nonogram.resizable(False, False)
    nonogram.eval('tk::PlaceWindow . center')
    nonogram.mainloop()


create_nonogram(answers_from_file("test.txt"))
