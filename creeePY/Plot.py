
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

        self.param = pd.read_csv(f'{files.param}/param.csv', sep = ';', index_col = 0)
        self.labels = pd.read_csv(f'{files.param}/labels.csv', sep = ';', index_col = 0)
        self.plot = pd.read_csv(f'{files.param}/plot.csv', sep = ';', index_col = 0)



#### Parameter functions


    def Load(self, table, sort = False):
        self.df = pd.read_csv(table, sep = ';')
        
        if sort == True:
            self.subcat = set(self.df[self.sort])
        return self.df


    def SetParam(self, **kwargs):
        self.__dict__.update(kwargs)


    def ParamPlot(self, n = 1, m = 1, **kwargs):
        plt.rcParams["font.family"] = self.fontFamily
        plt.rcParams["font.size"] = self.fontSize
        fig, axes = plt.subplots(nrows = n, ncols = m, figsize=(self.width, self.height), dpi = self.dpi, **kwargs)
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
            a = getattr(self, f'{it[1]}')
            

    def SetScatterParam(self, i, df, **kwargs):    
        listScatter = []
        for key in kwargs.keys():
            a = getattr(self, key)
            val = df.loc[i, kwargs[key]]
            listScatter.append(a[val])
        return listScatter


    def Combine(self, files, key, *fields):
        self.samples = self.Load(f'{files.input}/samples.csv')
        self.resume = self.Load(f'{files.input}/resume.csv')
        keys = [key]
        for e in fields:
            keys.append(e)
        self.df = self.resume.merge(self.samples[keys], on=key, how='outer')
        self.df.to_csv(f'{files.stats}/all.csv', sep = ';', index = None)


    def PlotXY(self, ax, df, xx, yy, colAnn, ann, fc, ec, m, s, alpha, c, cmap, vmin, vmax):

        df.index = np.arange(0, df.shape[0], 1)
        for i in df.index:
            x = df.loc[i, xx]
            y = df.loc[i, yy]

            if 'MinMax' in alpha and 'MinMax' not in s:
                a = df.loc[i, alpha]
                if c == 'no':
                    ls = self.SetScatterParam(i, df, facecolor = fc, edgecolor = ec, marker = m, size = s)
                    ax.scatter(x, y, facecolor = ls[0], edgecolor = ls[1], marker = ls[2], alpha = a, s = ls[3])
                else:
                    cc = df.loc[i, c]
                    ls = self.SetScatterParam(i, df, facecolor = fc, edgecolor = ec, marker = m, size = s, cmap = cmap)
                    ax.scatter(x, y, edgecolor = ls[1], marker = ls[2], alpha = a, s = ls[3], c = cc, cmap = ls[4], vmin = vmin, vmax = vmax)
            if 'MinMax' in s and 'MinMax' not in alpha:
                size = df.loc[i, s]
                if c == 'no':
                    ls = self.SetScatterParam(i, df, facecolor = fc, edgecolor = ec, marker = m, alpha = alpha)
                    ax.scatter(x, y, facecolor = ls[0], edgecolor = ls[1], marker = ls[2], alpha = ls[3], s = size)
                else:
                    cc = df.loc[i, c]
                    ls = self.SetScatterParam(i, df, facecolor = fc, edgecolor = ec, marker = m, alpha = alpha, cmap = cmap)
                    ax.scatter(x, y, edgecolor = ls[1], marker = ls[2], alpha = ls[3], s = size, c = cc, cmap = ls[4], vmin = vmin, vmax = vmax)
            elif 'MinMax' in s and 'MinMax' in alpha:
                size = df.loc[i, s]
                a = df.loc[i, alpha]
                if c == 'no':
                    ls = self.SetScatterParam(i, df, facecolor = fc, edgecolor = ec, marker = m)
                    ax.scatter(x, y, facecolor = ls[0], edgecolor = ls[1], marker = ls[2], alpha = alpha, s = size)
                else:
                    cc = df.loc[i, c]
                    ls = self.SetScatterParam(i, df, facecolor = fc, edgecolor = ec, marker = m, cmap = cmap)
                    ax.scatter(x, y, edgecolor = ls[1], marker = ls[2], alpha = alpha, s = size, c = cc, cmap = ls[3], vmin = vmin, vmax = vmax)
            else:
                #ls = self.SetScatterParam(i, df, facecolor = fc, edgecolor = ec, marker = m, size = s, alpha = alpha, c = c, cmap = cmap)
                if c == 'no':
                    ls = self.SetScatterParam(i, df, facecolor = fc, edgecolor = ec, marker = m, size = s, alpha = alpha)
                    ax.scatter(x, y, facecolor = ls[0], edgecolor = ls[1], marker = ls[2], s = ls[3], alpha = ls[4])
                else:
                    cc = df.loc[i, c]
                    ls = self.SetScatterParam(i, df, facecolor = fc, edgecolor = ec, marker = m, size = s, alpha = alpha, cmap = cmap)
                    ax.scatter(x, y, edgecolor = ls[1], marker = ls[2], s = ls[3], alpha = ls[4], c = cc, cmap = ls[5], vmin = vmin, vmax = vmax)
                #ax.scatter(x, y, facecolor = ls[0], edgecolor = ls[1], marker = ls[2], s = ls[3], alpha = ls[4], c = ls[5], cmap = ls[6])

            if ann != 'no' and df.loc[i, colAnn] in ann:
                ax.annotate(df.loc[i, colAnn], (x, y))

            
    def PlotTernary(self, files, T, L, R, df, facecolor, edgecolor, marker, labels = True):

        df = self.Load(f'{files.input}/{df}.csv')
        
        plt.rcParams["font.family"] = self.fontFamily
        plt.rcParams["font.size"] = self.fontSize                                       
        fig, ax = plt.subplots(1, 1, figsize=(self.width, self.height), dpi = self.dpi, subplot_kw=dict(projection="ternary"))

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

        ax.set_tlabel(T)
        ax.set_llabel(L)
        ax.set_rlabel(R)
        
        if labels == False:
            for ax in fig.get_axes():
                ax.label_outer()
            label = 'lab'
        else:
            label = ''

        self.Save(fig, f'{files.output}/TernaryPlot_{T}{L}{R}-{label}.png')

            
    def PlotScatterXYSave(self, files, X, Y, df, facecolor, edgecolor, marker, s, sep, xlim = None, ylim = None, ann = None, sort = None, c = None, cmap = None, vmin = 0, vmax = 0):

        df = pd.read_csv(f'{files.input}/{df}.csv', sep = sep)

        if sort != None:
            sort = sort.split('_')
            df = df[df[sort[0]] == sort[1]]


        fig, ax = self.ParamPlot(1, 1)
        
        for i in df.index:
            x = df.loc[i, X]
            y = df.loc[i, Y]
            
            if c == None:
                ls = self.SetScatterParam(i, df, facecolor = facecolor, edgecolor = edgecolor, marker = marker, size = s)
                ax.scatter(x, y, facecolor = ls[0], edgecolor = ls[1], marker = ls[2], s = ls[3])
            else:
                cc = df.loc[i, c]
                ls = self.SetScatterParam(i, df, facecolor = facecolor, edgecolor = edgecolor, marker = marker, size = s, cmap = cmap)
                print(cc, ls[4])
                #ax.scatter(x, y, c = cc, edgecolor = ls[1], marker = ls[2], s = ls[3], cmap = ls[4])
                ax.scatter(x, y, edgecolor = ls[1], marker = ls[2], c = cc, cmap = cmap, vmin = vmin, vmax = vmax)
            
            
            if ann == None:
                annot = ''
            else:
                t = df.loc[i, ann]
                ax.annotate(t, (x, y))
                annot = 'ann'

        if xlim != None:
            ax.set_xlim(xlim[0], xlim[1])
        if ylim != None:
            ax.set_ylim(ylim[0], ylim[1])
        
        ax.set_xlabel(X)
        ax.set_ylabel(Y)

        self.Save(fig, f'{files.output}/Plot_{X}{Y}{sort[1]}{annot}.png')


    def IterationPlot(self, files):

        self.ColumnsPlot(files)
        plot = self.plot
        
        for ind, xx, yy, px, py, dff, fc, ec, m, s, alpha, c, cmap, vmin, vmax, typ, proj, ann, xlim, ylim, sortType, sort, values, textbox, sharex, sharey, labels in zip(plot.id, plot.xx, plot.yy, plot.pX, plot.pY, plot.df, plot.facecolor, plot.edgecolor, plot.marker, plot.s, plot.alpha, plot.c, plot.cmap, plot.vmin, plot.vmax, plot.type, plot.proj, plot.annotate, plot.xlim, plot.ylim, plot.sorttype,  plot.sort, plot.sortvalues, plot.textbox, plot.shareX, plot.shareY, plot.labels):

            dfAll = self.Load(f'{files.input}/{dff}.csv')
        
            catX, colCatX, countCatX = self.readXY(xx, dfAll)
            catY, colCatY, countCatY = self.readXY(yy, dfAll)
            annT, colAnn, countAnn = self.readXY(str(ann), dfAll)

            fig, axes = self.ParamPlot(len(catX), len(catY), sharex = sharex, sharey = sharey)


            for catx, caty, ppx, ppy in list(product(catX, catY, [px], [py])):
            
                ax = self.SetAxes(fig, axes, catx, caty, catX, catY)

                if sortType == 'inner':
                    df = self.SortDataFrameInner(dfAll, sort, values)
                elif sortType == 'combine': 
                    df = self.SortDataFrameCombine(dfAll, sort, values)

                dcat = df[(df[colCatX] == catx) & (df[colCatY] == caty)]
                
                ddcat, ss, aalpha = self.SetSizeAlpha(dfAll, dcat, df, s, alpha)
                
                if c != 'no':
                    vvmin, vvmax = self.SetMinMaxCmap(dfAll, dcat, df, vmin, vmax)
                else:
                    vvmin = 'no'
                    vvmax = 'no'
                
                self.PlotXY(ax, dcat, ppx, ppy, colAnn, annT, fc, ec, m, ss, aalpha, c, cmap, vvmin, vvmax)
            
                if textbox == True:
                    ax.text(0, 0.9, f'{catx}, {caty}', transform = ax.transAxes)
                    lab = 'lab'
                else:
                    lab = 'no'
                
                if xlim != False:
                    xxlim = xlim.split('_')
                    ax.set_xlim(xxlim[0], xxlim[1])
                if ylim != False:
                    yylim = ylim.split('_')
                    ax.set_ylim(yylim[0], yylim[1])

                if annT == 'no':
                    annot = 'no'
                else:
                    annot = 'ann'

            if 'iter' not in catY:
                xa = len(catX)//2
                axes[xa, 0].set_ylabel(py)
                ya = len(catY)//2
                axes[xa, ya].set_xlabel(px)

            if labels == True:
                for ax in fig.get_axes():
                    ax.label_outer()

            print(colCatX, colCatY, px, py, annot)
            self.Save(fig, f'{files.output}/{ind}_{colCatX}-{colCatY}-{px}-{py}-{lab}-{annot}.png')


    def ColumnsPlot(self, files, plot = 'auto'):

        if plot == 'auto':
            plot = self.plot
        else:
            plot = pd.read_csv(f'{files.param}/plot.csv', sep = ';', index_col = 0)

        plot['id'] = plot.index

        X = []
        Y = []
        IND = []

        for ind, x, y, df in zip(plot.id, plot.x, plot.y, plot.df):

            dff = self.Load(f'{files.input}/{df}.csv')

            x = self.readPlotXY(x, dff)
            y = self.readPlotXY(y, dff)
            X, Y, IND = self.XY(X, Y, IND, x, y, ind)
        
        plot = pd.DataFrame(list(zip(IND, X, Y)), columns = ['ind', 'pX', 'pY'])
        plot = plot.drop_duplicates(keep = 'last')
        self.plot['ind'] = self.plot['id']
        self.plot = self.plot.merge(plot, on = 'ind', how = 'outer')
        del self.plot['id']
        self.plot.index = np.arange(0, self.plot.shape[0], 1)
        for i in self.plot.index:
            a = self.plot.loc[i, 'ind']
            self.plot.loc[i, 'id'] = f'{a}-{i}'
        self.plot.to_csv(f'{files.output}/plotConfig.csv', sep = ',')


    def readPlotXY(self, val, df):

        val = val.split('_')

        if 'auto' in val:                                       # toutes les valeurs d'une colonne donnée
            cat = [col for col in df.columns if col not in val[1:]]                       
        elif 'list' in val:                                   # une liste de valeurs dans une colonne donnée
            cat = val[1:]

        return cat


    def readXY(self, val, df):
        val = val.split('_')                                  # make a slice
        if 'auto' in val:                                     # toutes les valeurs d'une colonne donnée
            cat = list(set(df[val[1]]))                       
        elif 'list' in val:                                   # une liste de valeurs dans une colonne donnée
            cat = val[2:]
        elif 'value' in val:                                  # un seul plot
            cat = [1]
        elif 'iter' in val:                                   # plot itérant uniquement sur les valeurs de x et non y (les plots 2:3 pour 6 minéraux)
            cat = ['iter']
        elif 'no' in val:
            cat = ['no']
        
        countCat = np.arange(0, len(cat), 1)
        colCat = val[1] 

        return cat, colCat, countCat


    def XY(self, X, Y, IND, x, y, ind):
            
        b = list(product(x, y))
        xx = []
        yy = []
        for bb in b:
            xx.append(bb[0])
            yy.append(bb[1])

        ind = [ind] * len(yy)
        X = X + list(xx)
        Y = Y + list(yy)
        IND = IND + ind
        return X, Y, IND

   
    def SetAxes(self, fig, axes, catx, caty, catX, catY):
        if caty != 1 and caty != 'iter' :
            n = catX.index(catx)
            m = catY.index(caty)
            ax = axes[n, m]
        elif caty == 'iter':
            axes = fig.get_axes()
            n = catX.index(catx)
            ax = axes[n]
        elif caty == 1:
            ax = axes
        return ax


    def SetSizeAlpha(self, dfAll, dfCat, df, s, alpha):
        col = []
        for name, element in zip(['s', 'alpha'], [s, alpha]):
            val = element.split('_')
            if 'values' in val:                         # valeur de la colonne avec la colonne param
                cc = val[1]
            elif 'minmax' in val:                       # min et max indiqué : minmax_col_minSize_minValue_maxValue
                cc = val[1]
                mini = float(val[3])
                maxi = float(val[4] + mini)
                df[f'{name}MinMax'] = 1 - ((maxi - df[cc]) / maxi)
                if name == 's':
                    df[f'{name}MinMax'] = df[f'{name}MinMax'] * float(val[2])
                cc = f'{name}MinMax'
            elif 'auto' in val:                         # min et max de la colonne : recalcule sur 100% et multiplie pour la taille voulue
                if val[1] == 'df':
                    df = df
                elif val[1] == 'dfAll':
                    df = dfAll
                elif val[1] == 'dfCat':
                    df = dfCat
                cc = val[2]
                mini = np.min(df[cc])
                maxi = np.max(df[cc]) + mini
                df[f'{name}MinMax'] = 1 - ((maxi - df[cc]) / maxi)
                df[f'{name}MinMax'] = df[f'{name}MinMax'] * float(val[3])
                cc = f'{name}MinMax'
            else:
                cc = val[1]
            col.append(cc)
        s = col[0]
        alpha = col[1]
        df.to_csv('test.csv', sep = ';')
        return df, s, alpha


    def SetMinMaxCmap(self, dfAll, dfCat, df, vmin, vmax):
        col = []
        for name, element in zip(['vmin', 'vmax'], [vmin, vmax]):
            val = element.split('_')
            if 'minmax' in val:                         # valeur de la colonne avec la colonne param
                col.append(val[1])
            elif 'auto' in val:                         # min et max de la colonne : recalcule sur 100% et multiplie pour la taille voulue
                if val[1] == 'df':
                    df = df
                elif val[1] == 'dfAll':
                    df = dfAll
                elif val[1] == 'dfCat':
                    df = dfCat
                cc = val[2]

                if name == 'vmin':
                    v = np.min(df[cc])
                    col.append(v)
                elif name == 'vmax':
                    v = np.max(df[cc])
                    col.append(v)
        vmin = col[0]
        vmax = col[1]
        print(val[1], vmin, vmax)
        return vmin, vmax


    def SortDataFrameCombine(self, df, sort, values):
        sort = sort.split('_')
        values = values.split('_')
        ddf = pd.DataFrame()
        for s, val in zip(sort, values):
            d = df[df[s] == val]
            ddf = pd.concat([ddf, d])
        return ddf

    
    def SortDataFrameInner(self, df, sort, values):
        sort = sort.split('_')
        values = values.split('_')
        for s, val in zip(sort, values):
            df = df[df[s] == val]
        return df


    def Save(self, fig, title):
        if self.eps == False:
            plt.savefig(title, bbox_inches = 'tight', dpi = 400, pad_inches = 0)
        if self.eps == True:
            title = title.replace('.png', '.eps')
            plt.savefig(title, bbox_inches = 'tight', dpi = 400, pad_inches = 0, format = 'eps')
        fig.clear()
        plt.close(fig)
        plt.clf()
