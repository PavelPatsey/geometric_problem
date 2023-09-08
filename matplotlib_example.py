import matplotlib.pyplot as plt


def plot_points_and_line(x1, y1, x2, y2):
    # Рисуем точки
    plt.scatter([x1, x2], [y1, y2], color='red')

    # Соединяем точки линией
    plt.plot([x1, x2], [y1, y2], color='blue')

    # Рисуем график
    plt.show()


# Определяем координаты точек
x1, y1 = 1.5, 2.5
x2, y2 = 3.5, 4.5

# Вызываем функцию для отображения точек и линии
plot_points_and_line(x1, y1, x2, y2)
