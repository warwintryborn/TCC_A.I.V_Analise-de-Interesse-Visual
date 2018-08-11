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
    __RESOLUCAO = 100
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
        n = 1e5
        self.fig = PLT.figure(1)
        self.__x = self.__y = NP.linspace(0, self.__RESOLUCAO,
                                          self.__RESOLUCAO)  # Valor min, valor max, Numero de divisões
        X, Y = NP.meshgrid(self.__x, self.__y)  # Transforma em grid
        '''Quanto maior o numero de divisões mais qualidade a imagem tem'''

#        Z1 = ML.bivariate_normal(X, Y, 2, 2, 0, 0)
#        Z2 = ML.bivariate_normal(X, Y, 4, 1, 1, 1)

        self.__x = X.ravel()
        self.__y = Y.ravel()
        self.__heatArray = NP.zeros(
            self.__RESOLUCAO * self.__RESOLUCAO)  # NP.random.randn(400*400)#ZD.ravel() #Tem que ser um array com (Numero de divisões)^2

        self.__gridsize = 60
        PLT.subplot(111)

    def incrementa(self, x, y, raio):
        __heat = [8];

        if (x > self.__RESOLUCAO or y > self.__RESOLUCAO):
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
        PLT.hexbin(self.__x, self.__y, C=self.__heatArray, gridsize=self.__gridsize, cmap=CM.jet, bins=None)
        PLT.axis([self.__x.min(), self.__x.max(), self.__y.min(), self.__y.max()])

        cb = PLT.colorbar()
        cb.set_label('mean value')
        PLT.show()
        PLT.close();
        return;

    def teste_heat(self):
        self.__heatArray = NP.random.randn(self.__RESOLUCAO * self.__RESOLUCAO)#ZD.ravel() #Tem que ser um array com (Numero de divisões)^2

    def update_map(self):
        x = NP.linspace(0, 6 * NP.pi, 100)
        y = NP.sin(x)

        ax = self.fig.add_subplot(111)
        line1, = ax.plot(x, y, 'r-')  # Returns a tuple of line objects, thus the comma

        for phase in NP.linspace(0, 10 * NP.pi, 500):
            line1.set_ydata(NP.sin(x + phase))
            self.fig.canvas.draw()
            self.fig.canvas.flush_events()
        
if (__name__ == "__main__" ):
    hm = HeatMaping()
    hm.show_map();
