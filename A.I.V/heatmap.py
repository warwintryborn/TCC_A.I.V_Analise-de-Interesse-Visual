# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 18:34:19 2018

@author: ggoncalves
"""
import sys

from matplotlib import pyplot as PLT
from matplotlib import cbook as CBOOK
# from scipy.misc import imread
from matplotlib import mlab as ML
import numpy as NP


class HeatMap:
    __WIDTH = 30
    __HIGHT = 15
    __VALOR_INCREMENTAL = 4
    __VALOR_INCREMENTAL_PERIFERIA = __VALOR_INCREMENTAL/2
    __HEATTYPE = 'jet'
    __RAIO = 2
    IS_CHANGED = False;

    @property
    def resolucao(self):
        return self.__RESOLUCAO;

    @resolucao.setter
    def resolucao(self, value):
        self.__RESOLUCAO = int(value);

    @property
    def heatArray(self):
        return self.__heatValue

    @heatArray.setter
    def heatArray(self, value):
        if (value.size == self.__RESOLUCAO):
            self.__heatValue = value;

    def __init__(self):
        try:
            # datafile = CBOOK.get_sample_data('C:\Gustavo\Stuffs\GitHub\TCC\A.I.V\maua2.png')
            # img = PLT.imread(datafile)

            # create the figure
            PLT.rcParams['toolbar'] = 'None'
            self.fig = PLT.figure()
            PLT.set_cmap(self.__HEATTYPE)

            ax = self.fig.add_subplot(111)
            self.__heatValue = NP.zeros((self.__HIGHT, self.__WIDTH))
            self.im = ax.imshow(self.__heatValue,alpha=0.5)
            # self.im = ax.imshow(img,alpha=0.4)
            self.clb = self.fig.colorbar(self.im, ticks=[]);

            self.config_heat_fig();

            self.show_map();
        except:
            error = sys.exc_info()[0]
            print("Unexpected error:", error)

    def incrementa(self, x, y):

        if (0 > x > self.__WIDTH or 0 > y > self.__HIGHT):
            #Adicionar mensagem de erro!!
            return;

        self.__heatValue[x][y] += self.__VALOR_INCREMENTAL;  # centro

        for i in range(1, self.__RAIO):

            direita = x + i;
            esquerda = x - i;
            cima = y + i;
            baixo = y - i;

            if( direita < self.__HIGHT ):
                self.__heatValue[direita][y] += self.__VALOR_INCREMENTAL;  # direita
                if (cima < self.__WIDTH):
                    self.__heatValue[direita][cima] += self.__VALOR_INCREMENTAL_PERIFERIA;  # direita em cima
                if (0 < baixo):
                    self.__heatValue[direita][baixo] += self.__VALOR_INCREMENTAL_PERIFERIA;  # direita em baixo

            if( 0 < esquerda ):
                self.__heatValue[esquerda][y] += self.__VALOR_INCREMENTAL;  # esquerda
                if (cima < self.__WIDTH):
                    self.__heatValue[esquerda][cima] += self.__VALOR_INCREMENTAL_PERIFERIA;  # esquerda em cima
                if (0 < baixo):
                    self.__heatValue[esquerda][baixo] += self.__VALOR_INCREMENTAL_PERIFERIA;  # esquerda em baixo

            if( cima < self.__WIDTH ):
                self.__heatValue[x][cima] += self.__VALOR_INCREMENTAL;  # cima

            if( 0 < baixo):
                self.__heatValue[x][baixo] += self.__VALOR_INCREMENTAL;  # baixo

        self.IS_CHANGED = True;
        self.show_map();

        return;

    def show_map(self):
        try:
            self.im.set_array(self.__heatValue)
            self.fig.canvas.draw()

            vmax = self.__heatValue.max()
            vmin = self.__heatValue.min()

            self.clb.set_clim(vmin=vmin,vmax=vmax);

            self.IS_CHANGED = False;

            PLT.pause(0.01)
        except:
            error = sys.exc_info()[0]
            print("Unexpected error:", error)
        return

    def config_heat_fig(self):

        titulo_janela = PLT.gcf()
        titulo_janela.canvas.set_window_title('Análise de Interesse Visual - Heatmap vitrine')
        PLT.axis('off');
        PLT.suptitle("A.I.V.", fontsize=32);
        PLT.title("Vitrine", fontsize=12);

    def reset_map(self):
        self.__heatValue = NP.zeros((self.__HIGHT, self.__WIDTH))  # random.random((self.__HIGHT, self.__WIDTH))
        self.show_map();

if (__name__ == '__main__' ):

    hm = HeatMap()
    hm2 = HeatMap()

    hm.incrementa(5, 13)
    # hm.show_map()

    hm2.incrementa(10, 8)
    # hm2.show_map()

    # for i in range(30):
    #     for k in range(15):
    #         hm.incrementa(k, i)
    #         hm.show_map()

    hm.reset_map()
    hm2.reset_map();

    exit()
