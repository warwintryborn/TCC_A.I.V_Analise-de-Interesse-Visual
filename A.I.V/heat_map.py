# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 18:34:19 2018

@author: ggoncalves
"""
from matplotlib import pyplot as PLT
from matplotlib import cm as CM
from matplotlib import mlab as ML
import numpy as NP


class HeatMaping:
    __WIDTH = 30
    __HIGHT = 15
    __VALOR_INCREMENTAL = 5

    @property
    def resolucao(self):
        return self.__RESOLUCAO;

    @resolucao.setter
    def resolucao(self, value):
        self.__RESOLUCAO = int(value);

    @property
    def heatArray(self):
        return self.__heatArray

    @heatArray.setter
    def heatArray(self, value):
        if (value.size == self.__RESOLUCAO):
            self.__heatArray = value;

    def __init__(self):
        try:
            self.__heatArray = NP.random.random((self.__HIGHT, self.__WIDTH))
            # create the figure
            self.fig = PLT.figure()
            self.ax = self.fig.add_subplot(111)
            self.im = self.ax.imshow(self.__heatArray)
            PLT.show(block=False)
            PLT.pause(0.01)
        except:
            pass

    def incrementa(self, x, y, raio):
        __heat = [8];

        if (x > self.__RESOLUCAO or y > self.__RESOLUCAO):
            #Adicionar mensagem de erro!!
            return;

        local = (x * self.__RESOLUCAO + y * self.__RESOLUCAO)

        for i in range(0, raio):
            __heat[0] = local + i;  # direita
            __heat[1] = local - i;  # esquerda
            __heat[2] = local + i * self.__RESOLUCAO;  # cima
            __heat[3] = local - i * self.__RESOLUCAO;  # baixo
            __heat[4] = local + i + i * self.__RESOLUCAO;  # direita em cima
            __heat[5] = local - i + i * self.__RESOLUCAO;  # esquerda em cima
            __heat[6] = local + i - i * self.__RESOLUCAO;  # direita em baixo
            __heat[7] = local - i - i * self.__RESOLUCAO;  # esquerda em baixo

        for posicao in __heat:

            if (posicao > self.__RESOLUCAO or posicao < 0):
                continue;

            self.__heatArray[posicao] = self.__VALOR_INCREMENTAL;

        return;

    def show_map(self):
        try:
            #Transfor para numpy array
            self.__heatArray = NP.random.random((self.__HIGHT, self.__WIDTH))
            self.im.set_array(self.__heatArray)
            self.fig.canvas.draw()
            PLT.pause(0.01)
        except:
            pass
        return


    def teste_heat(self):
        self.__heatArray = NP.random.random((self.__HIGHT, self.__WIDTH))
        return


if (__name__ == '__main__' ):

    hm = HeatMaping()

    for i in range(100):
        hm.teste_heat()
        hm.show_map()