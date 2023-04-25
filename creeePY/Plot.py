
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mplc
import matplotlib as mpl
from colour import Color
from mpl_toolkits.axes_grid1 import make_axes_locatable
from itertools import product, combinations, chain
import matplotlib.gridspec as gridspec
import math
import os

    
class Plot():
    def __init__(self, files, **kwargs):
        
        self.__dict__.update(kwargs)

        self.param = pd.read_csv(f'{files.param}/param.txt', sep = '&', index_col = 0)
        self.labels = pd.read_csv(f'{files.param}/labels.txt', sep = '&', index_col = 0)
        self.plot = pd.read_csv(f'{files.param}/plot.txt', sep = '&', index_col = 0)



#### Parameter functions


    def Load(self, table, sort = False):
        self.df = pd.read_csv(table, sep = ',')
        
        if sort == True:
            self.subcat = set(self.df[self.sort])
        return self.df


    def SetParam(self, **kwargs):
        self.__dict__.update(kwargs)


    def ParamPlot(self, n, m):
        plt.rcParams["font.family"] = self.fontFamily
        plt.rcParams["font.size"] = self.fontSize
        fig, axes = plt.subplots(n, m, figsize=(self.width, self.height), dpi = self.dpi)
        return fig, axes
        
    
    def ColorScale(self, color1, color2 = 'white', step = 10):
        self.colorScale = mplc.LinearSegmentedColormap.from_list('', [color2, color1])
        
        
    def GetParam(self):
        dict = {}
        index = self.param.index
        param = ['color', 'facecolor', 'edgecolor', 'marker', 'alpha']
        for it in list(product(index, param)):
            dict[it[0]] = self.param.loc[it[0], it[1]]
            if hasattr(self, f'{it[1]}') == False:
                setattr(self, f'{it[1]}', dict)
            
        
    def Combine(self, key, *fields):
        self.samples = self.Load(f'{files.input}/samples.txt')
        self.resume = self.Load(f'{files.input}/resume.txt')

        keys = [key]

        for e in fields:
            keys.append(e)
        self.df = self.resume.merge(self.samples[keys], on=key, how='outer')


    def PlotXY(self, ax, df, X, Y, color, marker, alpha):
        for i in df.index():
            ax.scatter(self.df[X], self.df[Y], color = self.color[color], marker = self.marker[marker], alpha = alpha[alpha])


    def Plot(self):
        for i in self.plot:
            plotX = list(set(self.df[self.plot.loc[i, 'plotX']]))
            plotY = list(set(self.df[self.plot.loc[i, 'plotY']]))
            
            
            
        


    def Save(self, title):
        if self.eps == False:
            plt.savefig(title, bbox_inches = 'tight', dpi = 400)
        if self.eps == True:
            title = title.replace('.png', '.eps')
            plt.savefig(title, bbox_inches = 'tight', format = 'eps')
        plt.clf()
