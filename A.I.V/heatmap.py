# -*- coding: utf-8 -*-
"""
Created on Mon Jul 30 18:34:19 2018

@author: ggoncalves
"""
import datetime as dt;
import random
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

    @property
    def width(self):
        return self.__WIDTH;

    @property
    def higth(self):
        return self.__HIGHT;

    @property
    def heatArray(self):
        return self.__heatValue

    def get_titulo(self):
        return self.titulo

    def __init__(self, titulo=""):
        try:
            # datafile = CBOOK.get_sample_data('Vitrines/maua.png')
            # img = PLT.imread(datafile)
            self.titulo = titulo;
            # create the figure
            PLT.rcParams['toolbar'] = 'None'
            self.fig = PLT.figure(self.titulo)
            PLT.set_cmap(self.__HEATTYPE)

            ax = self.fig.add_subplot(111)
            self.__heatValue = NP.zeros((self.__HIGHT, self.__WIDTH))
            self.im = ax.imshow(self.__heatValue,alpha=0.5)
            # self.im = ax.imshow(img,alpha=0.4)
            self.clb = self.fig.colorbar(self.im, ticks=[]);

            self.config_heat_fig();

            self.reset_map();
        except:
            error = sys.exc_info()[0]
            print("Unexpected error:", error)

    def incrementa(self, coord):

        x = coord[0];
        y = coord[1];

        try:
            # self.__VALOR_INCREMENTAL = random.randrange(0,10)
            
            if x < 0:
                return
            if x >= self.__WIDTH:
                return
            if y < 0:
                return
            if y >= self.__HIGHT:
                return

            self.__heatValue[x][y] += self.__VALOR_INCREMENTAL;  # centro
            for i in range(1, self.__RAIO):

                direita = x + i;
                esquerda = x - i;
                cima = y + i;
                baixo = y - i;

                if( direita <= self.__HIGHT ):
                    self.__heatValue[direita][y] += self.__VALOR_INCREMENTAL;  # direita
                    if (cima <= self.__WIDTH):
                        self.__heatValue[direita][cima] += self.__VALOR_INCREMENTAL_PERIFERIA;  # direita em cima
                    if (0 < baixo):
                        self.__heatValue[direita][baixo] += self.__VALOR_INCREMENTAL_PERIFERIA;  # direita em baixo

                if( 0 < esquerda ):
                    self.__heatValue[esquerda][y] += self.__VALOR_INCREMENTAL;  # esquerda
                    if (cima <= self.__WIDTH):
                        self.__heatValue[esquerda][cima] += self.__VALOR_INCREMENTAL_PERIFERIA;  # esquerda em cima
                    if (0 < baixo):
                        self.__heatValue[esquerda][baixo] += self.__VALOR_INCREMENTAL_PERIFERIA;  # esquerda em baixo

                if( cima <= self.__WIDTH ):
                    self.__heatValue[x][cima] += self.__VALOR_INCREMENTAL;  # cima

                if( 0 < baixo):
                    self.__heatValue[x][baixo] += self.__VALOR_INCREMENTAL;  # baixo

            self.IS_CHANGED = True;
            self.show_map();
        except:
            error = sys.exc_info()[0]
            print("Unexpected error:", error, x ,y)

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
        PLT.title(self.titulo, fontsize=12);

    def reset_map(self):
        self.__heatValue = NP.zeros((self.__HIGHT, self.__WIDTH))  # random.random((self.__HIGHT, self.__WIDTH))
        self.show_map();

    def salve_map(self):
        try:
            extensao = ".png"
            time = dt.datetime.now().strftime("%Y-%m-%d");
            path = "Vitrines/imagens/{0}_{1}".format(self.titulo,time);
            self.fig.savefig(path + extensao);
            path = path.replace("imagens","numpy");
            NP.save(path,self.__heatValue);
        except:
            error = sys.exc_info()[0]
            print("Unexpected error:", error)

    def load_map(self):
        try:
            extensao = ".npy"
            time = dt.datetime.now().strftime("%Y-%m-%d");
            path = "Vitrines/numpy/{0}_{1}".format(self.titulo, time);
            self.__heatValue = NP.load(path + extensao);
            self.show_map();
        except:
            error = sys.exc_info()[0]
            print("Unexpected error:", error)


if (__name__ == '__main__' ):

    heatmap2 = HeatMap("Global");
    heatmap = HeatMap("Usuario");

    for i in range(heatmap.width):
        for k in range(heatmap.higth):
            heatmap.incrementa((k, i));
    for i in range(heatmap.width):
        for k in range(heatmap.higth):
            heatmap2.incrementa((k, i));

    heatmap.salve_map();
    heatmap2.salve_map();

    heatmap.reset_map()
    heatmap2.reset_map();

    heatmap.load_map();
    heatmap2.load_map();

    exit()
