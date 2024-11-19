import tkinter as tk
from fileinput import close
from tkinter import PhotoImage

# Використані кольори
white = "#F5F5F5"
green = "#00FF7F"
red = "#8B2252"

# задаємо основну сітку та необхідні розміри
answers = []
answers_file = open("test.txt","r")
for line in answers_file:
    line_answers = []
    for unit in line.split():
        line_answers.append(unit)
    answers.append(line_answers)
answers_file.close()
rows = len(answers)
cols = len(answers[0])
# максимальна кількість чисел збоку
def numbers_amount(size):
    if size%2:
        return size//2
    return size//2+1
rows_numbers_amount=numbers_amount(rows)
cols_numbers_amount=numbers_amount(cols)


# вікно програми
nonogram = tk.Tk()
nonogram.title("Nonogram")

main_menu = tk.Menu(nonogram)

pre_made_menu = tk.Menu(main_menu, tearoff=False)
pre_made_menu.add_command(label = "test", command=lambda: print("AAAAAA"))
main_menu.add_cascade(label ="Pre made", menu = pre_made_menu)

nonogram.configure(menu = main_menu)

# Запис кількості помилок
mistakes_count = 0
mistakes = tk.Label(nonogram, text =f"Mistakes: {mistakes_count}", font=('Arial', 18))
mistakes.pack(padx=20, pady=20)

# сітка для розміщення елементів
button_grid = tk.Frame(nonogram)
for row in range(rows+rows_numbers_amount):
    button_grid.rowconfigure(row, weight = 1)
for col in range(cols+cols_numbers_amount):
    button_grid.columnconfigure(col, weight = 1)

# знаходимо значення сітки
def numbers_search(checking):
    numbers = [[] for _ in range(rows)]
    for row in range(rows):
        count = 0
        for col in range(cols):
            if checking[row][col]!='0':
                count += 1
            elif count:
                numbers[row].append(count)
                count = 0
        if count:
            numbers[row].append(count)
    return numbers

rows_numbers = numbers_search(answers)
cols_numbers = numbers_search([[answers[j][i] for j in range(cols)] for i in range(rows)])

# додаємо записи вгорі та зліва
for row in range(rows):
    for col in range(len(rows_numbers[row])):
        number = tk.Label(button_grid, text=f"{rows_numbers[row][col]}")
        number.grid(row=row+rows_numbers_amount, column=col)

for col in range(cols):
    for row in range(len(cols_numbers[col])):
        number = tk.Label(button_grid, text=f"{cols_numbers[col][row]}")
        number.grid(row=row, column=col+cols_numbers_amount)



# Даний файл необхідний для задання розмірів сітки у пікселях
pixel = tk.PhotoImage(width=1, height=1)
# Клас для елементів поля
class Nonobutton:
    def __init__(self, colour):
        self.button = tk.Button(button_grid, relief='groove', bg=white,
                                image=pixel, height=50, width=50)
        self.colour = colour
        self.status = "no"

# Створюємо елементи основного поля
buttons = [[Nonobutton(answers[row][col]) for col in range(cols)] for row in range(cols)]
changes_permission = True

for row in range(rows):
    for col in range(cols):
        # Призначаємо кнопкам функції, які виконуються при натиску на ліву кнопку миші
        buttons[row][col].button.bind("<Button-1>", lambda e, button = buttons[row][col]: left_click(button))
        # та на праву кнопку миші
        buttons[row][col].button.bind("<Button-3>", lambda e, button = buttons[row][col]: right_click(button))
        # Додаємо елементи до сітки
        buttons[row][col].button.grid(row=row+rows_numbers_amount, column=col+cols_numbers_amount, sticky=tk.W + tk.E)
button_grid.pack(fill="x", padx = 20)

# Перевірка перемоги користувача
# якщо усі клітинки ігрового поля, відповідні до значень матриці відповідей
# мають статус "розварбовано" значить користувач знайшов усі необхідні клітинки
def check_win():
    for row in range(rows):
        for col in range(cols):
            # якщо хоч для однієї клітинки ця умова не виконується
            # припиняємо перевірку
            if answers[row][col]!='0' and buttons[row][col].status != "color":
                return
    # забороняємо подальше внесення змін до поля
    global changes_permission
    changes_permission = False
    # виводимо повідомлення про виграш
    win = tk.Label(nonogram, text ="You won!", font=('Arial', 18))
    win.place(relx=0.5, rely=0.6, anchor="center")


# ліва кнопка миші відповідає за розфарбовування клітинок
def left_click(button: Nonobutton):
    if button.status=="no" and changes_permission:
        if button.colour != '0':
            button.button.configure(bg=button.colour)
            button.status = "color"
            check_win()
        else:
            button.button.configure(bg=red)
            button.status = "wrong"
            global mistakes_count
            mistakes_count+=1
            mistakes.configure(text=f"Mistakes: {mistakes_count}")

# права кнопка миші відповідає за встановлення допоміжних позначок
x_image = PhotoImage(file = r"x.png")
def right_click(button: Nonobutton):
    if changes_permission:
        if button.status == "no":
            button.button.configure(image=x_image)
            button.status = "x"
        elif button.status == "x":
            button.button.configure(image=pixel)
            button.status = "no"

nonogram.mainloop()