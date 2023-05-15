
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.colors as mplc
import matplotlib as mpl
import mpltern
from colour import Color
from mpl_toolkits.axes_grid1 import make_axes_locatable
from itertools import product, combinations, chain
import matplotlib.gridspec as gridspec
import math
import os

    
class Plot():
    def __init__(self, files, **kwargs):
        
        self.__dict__.update(kwargs)

        self.param = pd.read_csv(f'{files.param}/param.csv', sep = '&', index_col = 0)
        self.labels = pd.read_csv(f'{files.param}/labels.csv', sep = '&', index_col = 0)
        self.plot = pd.read_csv(f'{files.param}/plot.csv', sep = '&', index_col = 0)



#### Parameter functions


    def Load(self, table, sort = False):
        self.df = pd.read_csv(table, sep = '&')
        
        if sort == True:
            self.subcat = set(self.df[self.sort])
        return self.df


    def SetParam(self, **kwargs):
        self.__dict__.update(kwargs)


    def ParamPlot(self, n, m, **kwargs):
        plt.rcParams["font.family"] = self.fontFamily
        plt.rcParams["font.size"] = self.fontSize
        fig, axes = plt.subplots(n, m, figsize=(self.width, self.height), dpi = self.dpi, **kwargs)
        return fig, axes
        
    
    def ColorScale(self, color1, color2 = 'white', step = 10):
        self.colorScale = mplc.LinearSegmentedColormap.from_list('', [color2, color1])
        
        
    def GetParam(self):
        index = self.param.index
        param = self.param.columns
        for it in list(product(index, param)):
            if hasattr(self, f'{it[1]}') == False:
                a = {}
                setattr(self, f'{it[1]}', a)
            a = getattr(self, f'{it[1]}')
            a[it[0]] = self.param.loc[it[0], it[1]]
            setattr(self, f'{it[1]}', a)
            

    def SetScatterParam(self, i, df, **kwargs):    
        listScatter = []
        for key in kwargs.keys():
            a = getattr(self, key)
            val = df.loc[i, kwargs[key]]
            listScatter.append(a[val])
        return listScatter


    def Combine(self, key, *fields):
        self.samples = self.Load(f'{files.input}/samples.txt')
        self.resume = self.Load(f'{files.input}/resume.txt')

        keys = [key]

        for e in fields:
            keys.append(e)
        self.df = self.resume.merge(self.samples[keys], on=key, how='outer')


    def PlotXY(self, ax, df, X, Y, facecolor, edgecolor, marker, alpha = 1):
        for i in df.index():
            ax.scatter(self.df[X], self.df[Y], facecolor = self.color[color], marker = self.marker[marker], alpha = alpha[alpha])


    def Plot(self):
        for i in self.plot:
            plotX = list(set(self.df[self.plot.loc[i, 'plotX']]))
            plotY = list(set(self.df[self.plot.loc[i, 'plotY']]))
            
            
    def PlotTernary(self, files, T, L, R, df, facecolor, edgecolor, marker):

        df = self.Load(f'{files.input}/{df}.csv')
        
        fig, ax = self.ParamPlot(1, 1, subplot_kw=dict(projection="ternary"))
        
        for i in df.index:
            top = df.loc[i, T]
            left = df.loc[i, L]
            right = df.loc[i, R]

            ls = self.SetScatterParam(i, df, facecolor = facecolor, edgecolor = edgecolor, marker = marker )

            if ls[2] in ['*', '.']:
                self.s = 450
            else:
                self.s = 300


            ax.scatter(top, left, right, facecolor = ls[0], edgecolor = ls[1], marker = ls[2], s = self.s)
            #print(ls)
            #print(df.loc[i])

        ax.set_tlabel(T)
        ax.set_llabel(L)
        ax.set_rlabel(R)

        self.Save(f'{files.output}/TernaryPlot_{T}{L}{R}.png')

            
    def PlotScatterXY(self, files, X, Y, df, facecolor, edgecolor, marker, sep, sort = None):

        df = pd.read_csv(f'{files.input}/{df}.csv', sep = ',')
        
        if sort != None:
            df = df[df[sort[0]] == sort[1]]


        fig, ax = self.ParamPlot(1, 1)
        
        for i in df.index:
            x = df.loc[i, X]
            y = df.loc[i, Y]
            t = df.loc[i, 'cat']

            ls = self.SetScatterParam(i, df, facecolor = facecolor, edgecolor = edgecolor, marker = marker )

            if ls[2] in ['*', '.']:
                self.s = 450
            else:
                self.s = 300

            ax.scatter(x, y, facecolor = ls[0], edgecolor = ls[1], marker = ls[2], s = self.s)
            ax.annotate(t, (x, y))
            #print(ls)
            #print(df.loc[i])

        ax.set_xlabel(X)
        ax.set_ylabel(Y)

        self.Save(f'{files.output}/Plot_{X}{Y}{sort[1]}ann.png')


    def PlotScatterXY(self, files, X, Y, df, facecolor, edgecolor, marker, sep, sort = None):

        df = pd.read_csv(f'{files.input}/{df}.csv', sep = ',')
        
        if sort != None:
            df = df[df[sort[0]] == sort[1]]


        fig, ax = self.ParamPlot(1, 1)
        
        for i in df.index:
            x = df.loc[i, X]
            y = df.loc[i, Y]
            t = df.loc[i, 'cat']

            ls = self.SetScatterParam(i, df, facecolor = facecolor, edgecolor = edgecolor, marker = marker )

            if ls[2] in ['*', '.']:
                self.s = 450
            else:
                self.s = 300

            ax.scatter(x, y, facecolor = ls[0], edgecolor = ls[1], marker = ls[2], s = self.s)
            ax.annotate(t, (x, y))
            #print(ls)
            #print(df.loc[i])

        ax.set_xlabel(X)
        ax.set_ylabel(Y)

        self.Save(f'{files.output}/Plot_{X}{Y}{sort[1]}ann.png')


    def ColumnsPlot(self, files, plot = 'auto'):

        plot = self.Load(f'{files.param}/plot.csv')

        X = []
        Y = []
        IND = []

        for x, y, ind in zip(plot.pX, plot.pY, plot.id):

            df = self.Load(f'{files.output}/{df.csv}')

            if x == 'auto' and y == 'auto':
                X, Y, IND = self.XY(X, Y, IND, df.X. df.Y, ind)
            if x == 'auto' and y != 'auto':
                X, Y, IND = self.XY(X, Y, IND, df.X, y, ind)
            if x != 'auto' and y == 'auto':
                X, Y, IND = self.XY(X, Y, IND, x, df.Y, ind)
        

        self.plot pd.DataFrame(list(zip(IND, X, Y)), columns = ['id', 'X', 'Y'])
        self.plot = self.plot.merge(plot, on = 'id', how = 'outer')


    def XY(self, X, Y, IND, x, y, ind):
            
        xx, yy = list(product(x, y))
        ind = [ind] * len(yy)
        X = X + xx
        Y = Y + yy
        IND = IND + ind
        return X, Y, IND

    
    def Iterate(self, files):


        for x, y in zip(self.plot.X,):

            




    def Save(self, title):
        if self.eps == False:
            plt.savefig(title, bbox_inches = 'tight', dpi = 400)
        if self.eps == True:
            title = title.replace('.png', '.eps')
            plt.savefig(title, bbox_inches = 'tight', format = 'eps')
        plt.clf()
