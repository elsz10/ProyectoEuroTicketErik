import matplotlib.pyplot as plt
import numpy as np


class Grafico:
    def __init__(self):
        pass

    def show_grafic(self, names, views):
        x = np.array(names)
        y = np.array(views)

        plt.bar(x,y)
        plt.show()