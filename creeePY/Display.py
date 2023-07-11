import random
import pandas as pd
import numpy as np
from itertools import product
import matplotlib.pyplot as plt
import matplotlib.colors as mplc
import matplotlib.patches as patches
from matplotlib.collections import PatchCollection
from matplotlib.backend_bases import MouseButton
import matplotlib.patheffects as patheffects
import matplotlib as mpl
from colour import Color
from mpl_toolkits.axes_grid1 import make_axes_locatable
from matplotlib.ticker import (AutoMinorLocator, MultipleLocator)
import math
import os
from matplotlib.patches import Rectangle

    
class Display():
    def __init__(self, files, **kwargs):
        
        self.__dict__.update(kwargs)

        self.param = pd.read_csv(f'{files.param}/param.csv', sep = ';', index_col = 0)
        
        self.samples  = pd.read_csv(f'{files.folder}/EBSD.csv', sep = ';', index_col = 0)
        
        self.unit = {'um': 0, 'mm': 3, 'cm': 4, 'dm': 5, 'm': 6}
        self.scale = {'1': 'um', '2': 'um', '3': 'mm', '4': 'cm', '5': 'dm', '6': 'm'}

#### Parameter functions 


    def Load(self, table, sort = False):
        self.df = pd.read_csv(table, sep = ';')
        if sort == True:
            self.subcat = set(self.df[self.sort])
        return self.df


    def SetParam(self, **kwargs):
        self.__dict__.update(kwargs)
        
        
    def Iteration(self, files, func, iterMineral = False):
        for c in files.cat:
            if iterMineral == False:
                func(files, c)

            if iterMineral == True:
                for ssc in files.sscat:
                    if os.path.exists(f'{files.input}/{c}_{ssc}_{self.task}.csv'):
                        func(files, c, ssc)
        
    
    def ParamPlot(self):
        plt.rcParams["font.family"] = self.fontFamily
        plt.rcParams["font.size"] = self.fontSize
        fig, ax = plt.subplots(figsize=(self.width, self.height), dpi = self.dpi)
        return fig, ax
        
        
    def ColorScale(self, color1, min, max, color2 = 'white', step = 10):
        self.colorScale = mplc.LinearSegmentedColormap.from_list('', [color2, color1])
        self.normScale = mpl.colors.Normalize(vmin = min, vmax = max)
        self.cmap = mpl.cm.ScalarMappable(norm=self.normScale, cmap=self.colorScale)


#### Accessory plot functions

    def GetOrder(self, a):
        i = 1
        b = 100
        while b>10:
            b = a/(10**i)
            i += 1
        return i-1
        
        
    def CorrectBar(self, bar, length):
    
        barLength = int(bar.split(' ')[0])
        barUnit = bar.split(' ')[1]
        barLengthScale = barLength * 10**self.unit[barUnit]
        
        if barLengthScale > length:
            if self.unit[barUnit] > self.GetOrder(length):
                barUnit = self.unit[self.GetOrder(length)]
                barLengthScale = barLength * 10**self.unit[barUnit]
            else:
                barLength = length*0.75
                barUnit = self.scale[str(self.GetOrder(barLength))]
                barLength = barLength/(10**self.GetOrder(barLength))
                barLength = int(barLength)
                barLengthScale = barLength * 10**self.unit[barUnit]

        return barLengthScale, barLength, barUnit
        

    def barScale(self, cat, ax, df, bar, text = None, gap = None):
        """Création de la barre d'échelle pour chaque graph"""
    
        # resolution, length and height of sample
        XCells = self.samples.loc[cat, 'XCells']        # number of points
        YCells = self.samples.loc[cat, 'YCells']        # number of points
        step = self.samples.loc[cat, 'XStep']           # resolution (microns /
        
        Xlength = step * XCells                         # microns
        Ylength = step * YCells                         # microns
        
        Xlength = np.max(df['x']) - np.min(df['x'])

        # gap verification
        if gap == None:
            mapLength = np.max(df['x']) - np.min(df['x'])
            gap = mapLength/60
            
        # bar length (in microns)
        barLengthScale, barLength, barUnit = self.CorrectBar(bar, Xlength)
        #print(cat, Xlength, barLengthScale, barLength, barUnit)
        
        x = [np.min(df['x']) + gap, np.min(df['x']) + gap + barLengthScale ]
        y = [np.min(df['y']) + gap, np.min(df['y']) + gap]

        # text position
        if text == None:
            xText = x[0] + barLengthScale / 2
            yText = y[0] + gap
            text = f'{barLength} {barUnit}'
            halignment = 'center'
            valignment = 'center_baseline'
        else:
            xText = x[0]
            yText = y[0] + gap
            text = f'{text}, {barLength} {barUnit}'
            halignment = 'left'
            valignment = 'center_baseline'

        # background
        ax.add_patch(Rectangle((x[0] - gap/2, y[0] - gap/2), barLengthScale + gap, gap*2.5, facecolor = 'white', edgecolor = 'black', linewidth = 1))
        # bar
        ax.plot(x, y, color = 'black', linewidth = 1)
        # legend
        ax.text(xText, yText, text, horizontalalignment=halignment, verticalalignment=valignment)
        
        # graduations
        grad = self.grad
        step = barLengthScale/grad
        steps = np.arange(0, grad+1, 1)
        for i in steps:
            xc = [x[0] + i*step, x[0] + i*step]
            yc = [y[0] - gap/5, y[0] + gap/5]
            ax.plot(xc, yc, 'black', linewidth = 1)
            
        return gap


    def PlotPatch(self, ax, cat, df, res, linewidth = 0, edgecolor = 'white', facecolor = 'red', cmap = None, norm = 'norm', array = 'array', alpha = 1):
        xx = df['x'].to_numpy()
        yy = df['y'].to_numpy()
        patch = []
        for x, y in zip(xx, yy):
            rect = patches.Rectangle((x, y), res, res)
            patch.append(rect)

        if cmap == None:
            ax.add_collection(PatchCollection(patch, linewidth = linewidth, edgecolor=edgecolor, facecolor=facecolor, alpha = alpha))
        else:
            collection = PatchCollection(patch, linewidth = linewidth, cmap = cmap, norm = norm, alpha = alpha)
            collection.set_array(df[array])
            ax.add_collection(collection)

        return ax
        
        
    def PlotPoints(self, files, cat, ax, gap, minX = 0, maxX = 0, minY = 0, maxY = 0):
        self.Load(f'{files.output}/points.csv')
        self.df = self.df[self.df['point'] == 'data']
        self.df.index = np.arange(0, self.df.shape[0], 1)
        self.df['id'] = self.df.index
        self.df.to_csv(f'{files.output}/pointsId.csv', sep = ';', index = None)
        self.df = self.df[self.df['cat'] == cat]
        
        if minX != None:
            self.df = self.df[(self.df['xdata'] > minX) & (self.df['xdata'] < maxX)]
            self.df = self.df[(self.df['ydata'] > minY) & (self.df['ydata'] < maxY)]
        
        for i in self.df.index:
            x = float(self.df.loc[i, 'xdata'])
            y = float(self.df.loc[i, 'ydata'])
            ax.scatter(x, y, s = 400, marker = 'X', facecolor = 'white', edgecolor = 'purple')
            ax.text(x + 3*gap/4, y + 3*gap/4, i, fontsize = 28, color='white', path_effects=[patheffects.withStroke(linewidth=3, foreground='purple')])
        return ax
        
        
    def ticks(self, ax):
        locs  = ax.get_yticks()
        labels = ax.get_yticklabels()
        r = 1
        labels = [str(round((loc/np.sum(self.weights))*100, r)) for loc in locs]
        #while len(set(labels)) != len(labels):
        #    labels = [str(round((loc/np.sum(self.weights))*100, r)) for loc in locs]
        #    r += 1
        ax.set_yticks(locs, labels = labels)


    def CombineDataframes(self, df1, df2, left_on, right_on, name):
        """Safe jointure of dataframes"""
        df2.index = df2[right_on]
        try:
            for i in df2.index:
                df1.loc[df1[left_on] == i, name] = df2.loc[i, name]
        except:
            pass
    
        return df1
        

    def Save(self, fig, title):
        if self.eps == False:
            plt.tight_layout()
            plt.savefig(title, dpi = self.dpi, bbox_inches = 'tight', pad_inches = 0)
        if self.eps == True:
            title = title.replace('.png', '.eps')
            plt.savefig(title, dpi = self.dpi, bbox_inches = 'tight', pad_inches = 0, format = 'eps')
        fig.clear()
        plt.close(fig)
        plt.clf()


#### Plot functions


    def PhasesMap(self, files, cat):
        res = self.samples.loc[cat, 'XStep']
        fig, ax = self.ParamPlot()
        for ssc in files.sscat:
            if os.path.exists(f'{files.input}/{cat}_{ssc}_EBSD.csv') and ssc != 'all':
                self.Load(f'{files.input}/{cat}_{ssc}_EBSD.csv')
                ax = self.PlotPatch(ax, cat, self.df, res, linewidth = 0, edgecolor = self.param.loc[ssc, 'edgecolor'], facecolor = self.param.loc[ssc, 'facecolor'], cmap = None, norm = 'norm')

        if os.path.exists(f'{files.input}/{cat}_Boundaries.csv'):
            self.Load(f'{files.input}/{cat}_Boundaries.csv')
            ax = self.PlotPatch(ax, cat, self.df, res, linewidth = 0, edgecolor = 'black', facecolor = 'black', cmap = None, norm = 'norm')
                    
        self.barScale(cat, ax, self.df, self.barLegend, text = self.text)
          
        plt.axis('off')
        plt.axis('scaled')

        self.Save(fig, f'{files.output}/{cat}_PhasesMap.png')
 
 
    def PointsMap(self, files, cat):
        points = self.Load(f'{files.output}/points.csv')
        zones = points[(points['point'] == 'zone') & (self.df['cat'] == cat)]
        zones['count'] = np.arange(1, zones.shape[0]+1, 1)
        count = np.arange(0, zones.shape[0] + 3, 3)

        res = self.samples.loc[cat, 'XStep']
        fig, ax = self.ParamPlot()
        for ssc in files.sscat:
            if os.path.exists(f'{files.input}/{cat}_{ssc}_EBSD.csv') and ssc != 'all':
                self.Load(f'{files.input}/{cat}_{ssc}_EBSD.csv')
                ax = self.PlotPatch(ax, cat, self.df, res, linewidth = 0, edgecolor = self.param.loc[ssc, 'edgecolor'], facecolor = self.param.loc[ssc, 'facecolor'], cmap = None, norm = 'norm')
                
        if os.path.exists(f'{files.input}/{cat}_Boundaries.csv'):
            self.Load(f'{files.input}/{cat}_Boundaries.csv')
            ax = self.PlotPatch(ax, cat, self.df, res, linewidth = 0, edgecolor = 'black', facecolor = 'black', cmap = None, norm = 'norm')

        gap = self.barScale(cat, ax, self.df, self.barLegend, text = self.text)
        
        for i in range(0, len(count)-1):
            xy = zones[(zones['count'] > count[i]) & (zones['count'] < count[i+1]+1)]
            ax.plot([np.min(xy['xdata']), np.max(xy['xdata'])], [np.max(xy['ydata']), np.max(xy['ydata'])], color = 'white')
            ax.plot([np.min(xy['xdata']), np.max(xy['xdata'])], [np.min(xy['ydata']), np.min(xy['ydata'])], color = 'white')
            ax.plot([np.max(xy['xdata']), np.max(xy['xdata'])], [np.min(xy['ydata']), np.max(xy['ydata'])], color = 'white')
            ax.plot([np.min(xy['xdata']), np.min(xy['xdata'])], [np.min(xy['ydata']), np.max(xy['ydata'])], color = 'white')
            ax.text(np.min(xy['xdata']) + gap/2, np.max(xy['ydata']) - 5*gap/2, i, color='white', fontsize = 36)

        #self.Load(f'{files.output}/points.csv')
        plt.axis('off')
        plt.axis('scaled')
        self.Save(fig, f'{files.output}/{cat}_ZonesMap.png')
        
        
        for i in range(0, len(count)-1):
            xy = zones[(zones['count'] > count[i]) & (zones['count'] < count[i+1]+1)]
            minX = int(np.min(xy['xdata']))
            maxX = int(np.max(xy['xdata']))
            minY = int(np.min(xy['ydata']))
            maxY = int(np.max(xy['ydata']))
            
            fig, ax = self.ParamPlot()
            for ssc in files.sscat:
                if os.path.exists(f'{files.input}/{cat}_{ssc}_EBSD.csv') and ssc != 'all':
                    self.Load(f'{files.input}/{cat}_{ssc}_EBSD.csv')
                    self.df = self.df[(self.df['x'] > minX) & (self.df['x'] < maxX)]
                    self.df = self.df[(self.df['y'] > minY) & (self.df['y'] < maxY)]
                    #ax = self.PlotPatch(ax, cat, self.df, res, linewidth = 0, edgecolor = self.param.loc[ssc, 'edgecolor'], facecolor = self.param.loc[ssc, 'facecolor'], cmap = None, norm = 'norm', alpha = 0.6)
                    ax = self.PlotPatch(ax, cat, self.df, res, linewidth = 0, edgecolor = self.param.loc[ssc, 'edgecolor'], facecolor = self.param.loc[ssc, 'facecolor'], cmap = None, norm = 'norm', alpha = 1)
                    
            if os.path.exists(f'{files.input}/{cat}_Boundaries.csv'):
                self.Load(f'{files.input}/{cat}_Boundaries.csv')
                self.df = self.df[(self.df['x'] > minX) & (self.df['x'] < maxX)]
                self.df = self.df[(self.df['y'] > minY) & (self.df['y'] < maxY)]
                #ax = self.PlotPatch(ax, cat, self.df, res, linewidth = 0, edgecolor = 'black', facecolor = 'dimgray', cmap = None, norm = 'norm')
                ax = self.PlotPatch(ax, cat, self.df, res, linewidth = 0, edgecolor = 'black', facecolor = 'black', cmap = None, norm = 'norm')

            gap = self.barScale(cat, ax, self.df, f'12 mm', text = self.text)       # 1750 = ecran de la microsonde
            
            ax.text(np.min(xy['xdata']) + gap/2, np.max(xy['ydata']) - 5*gap/2, i, color='white', fontsize = 46)
   
            ax = self.PlotPoints(files, cat, ax, gap, minX = np.min(xy['xdata']), maxX = np.max(xy['xdata']), minY = np.min(xy['ydata']), maxY = np.max(xy['ydata']))
            
            if self.quadri == True:
                ax.xaxis.set_major_locator(MultipleLocator(1750))
                ax.yaxis.set_major_locator(MultipleLocator(1750))
                ax.grid(visible=None, which='major', axis='both', color = 'black')
                quadri = 'Quadri'
            elif self.quadri == False:
                ax.axis('off')
                quadri = ''
                            
            ax.axis('scaled')
            self.Save(fig, f'{files.output}/{cat}_ZonesMap{quadri}-{i}.png')
            
 
    def SelectPoints(self, files, cat):
        fig = plt.figure()
        for ssc in files.sscat:
            if os.path.exists(f'{files.input}/{cat}_{ssc}_EBSD.csv') and ssc != 'all':
                self.Load(f'{files.input}/{cat}_{ssc}_EBSD.csv')
                plt.scatter(self.df['x'], self.df['y'], color = self.param.loc[ssc, 'facecolor'], s = 0.005)
        if os.path.exists(f'{files.input}/{cat}_Boundaries.csv'):
            self.Load(f'{files.input}/{cat}_Boundaries.csv')
            plt.scatter(self.df['x'], self.df['y'], color = 'black', s = 0.005, picker=True, pickradius=2)
        plt.axis('off')
        plt.axis('scaled')
        self.output = files.output
        self.cat = cat
        def click(event):
            print(f'{self.cat}&{event.button}&{event.x}&{event.y}&{event.xdata}&{event.ydata}')
            if os.path.exists(f'{files.output}/points.csv') == False:
                with open(f'{self.output}/points.csv', 'w') as file:
                    file.write('cat&point&x&y&xdata&ydata\n')
            
            if event.dblclick:
                plt.scatter(event.xdata, event.ydata, facecolor = 'white', edgecolor = 'green', marker = 'X', s = 50)
                point = 'zone'
            elif event.button == 1:
                plt.scatter(event.xdata, event.ydata, facecolor = 'black', edgecolor = 'red', marker = 'X', s = 50)
                point = 'click'
            elif event.button == 3:
                plt.scatter(event.xdata, event.ydata, facecolor = 'white', edgecolor = 'purple', marker = 'X', s = 50)
                point = 'data'
                
            with open(f'{self.output}/points.csv', 'a') as file:
                file.write(f'{self.cat}&{point}&{event.x}&{event.y}&{event.xdata}&{event.ydata}\n')
                
        cid = fig.canvas.mpl_connect('button_press_event', click)
        plt.show()


    def BoundariesMap(self, files, cat):
        res = self.samples.loc[cat, 'XStep']
        fig, ax = self.ParamPlot()
        if os.path.exists(f'{files.input}/{cat}_Boundaries.csv'):
            self.Load(f'{files.input}/{cat}_Boundaries.csv')
            ax = self.PlotPatch(ax, cat, self.df, res, linewidth = 0, edgecolor = 'black', facecolor = 'black', cmap = None, norm = 'norm')
            
            self.Load(f'{files.input}/{cat}_InnerBoundaries.csv')
            ax = self.PlotPatch(ax, cat, self.df, res, linewidth = 0, edgecolor = 'black', facecolor = 'blue', cmap = None, norm = 'norm')
            
            self.barScale(cat, ax, self.df, self.barLegend, text = self.text)
            
            plt.axis('off')
            plt.axis('scaled')
            self.Save(fig, f'{files.output}/{cat}_BoundariesMap.png')
            

    def FieldMap(self, files, cat):
        res = self.samples.loc[cat, 'XStep']
        fig, ax = self.ParamPlot()
                
        ebsd = self.Load(f'{files.input}/{cat}_all_EBSD.csv')
        if self.field not in self.df.columns:
            grains = self.Load(f'{files.input}/{cat}_all_Grains.csv')
            ebsd = ebsd.merge(grains, left_on='grain', right_on='id' , how='outer')
        
        if self.minimum == 'all':
            self.minimum = np.min(ebsd[self.field])
        if self.maximum == 'all':
            self.maximum = np.max(ebsd[self.field])
        
        sscat = [ssc for ssc in files.sscat if ssc != 'all']
        sscat = [ssc for ssc in sscat if ssc != 'notIndexed']

        for ssc in sscat:
            if os.path.exists(f'{files.input}/{cat}_{ssc}_EBSD.csv'):
                ebsd = self.Load(f'{files.input}/{cat}_{ssc}_EBSD.csv')
                
                if self.field not in self.df.columns:
                    grains = self.Load(f'{files.input}/{cat}_{ssc}_Grains.csv')
                    ebsd = ebsd.merge(grains, left_on='grain', right_on='id' , how='outer')
                    print(ebsd.columns)
                if self.color == 'sscat':
                    self.ColorScale(self.param.loc[ssc, 'color'], min = self.minimum, max = self.maximum, step = int(self.maximum - self.minimum))
                else:
                    self.ColorScale(self.color, min = self.minimum, max = self.maximum, step = int(self.maximum - self.minimum))
                    
                ax = self.PlotPatch(ax, cat, ebsd, res, linewidth = 0, edgecolor = 'black', facecolor = 'black', cmap = self.colorScale, norm = self.normScale, array = self.field)

        if self.boundaries == True:
            self.Load(f'{files.input}/{cat}_Boundaries.csv')
            ax = self.PlotPatch(ax, cat, self.df, res, linewidth = 0, edgecolor = 'black', facecolor = 'black', cmap = None, norm = 'norm')
            boundaries = 'Boundaries'
        else:
            boundaries = 'Noboundaries'
            
        self.barScale(cat, ax, self.df, self.barLegend, text = self.text)
        
        plt.axis('off')
        plt.axis('scaled')
        self.Save(fig, f'{files.output}/{cat}_Field{self.field}{boundaries}Map.png')
        
   

    def SortMap(self, files, cat):
        res = self.samples.loc[cat, 'XStep']
        fig, ax = self.ParamPlot()
        for ssc in files.sscat:
            if os.path.exists(f'{files.input}/{cat}_{ssc}_Grains.csv'):
            
                grains = self.Load(f'{files.input}/{cat}_{ssc}_Grains.csv', sort = True)
                ebsd = self.Load(f'{files.input}/{cat}_{ssc}_EBSD.csv')
                
                ebsd = ebsd.merge(grains, left_on = 'grain', right_on = 'id', how = 'outer')

                subcat = [s for s in self.subcat if s != 'all']
                
                for s in subcat:
                    sub = ebsd[ebsd[f'{self.sort}'] == s]
                    xx = sub['x'].to_numpy()
                    yy = sub['y'].to_numpy()
                    patch = []
                    for x, y in zip(xx, yy):
                        rect = patches.Rectangle((x, y), res, res)
                        patch.append(rect)
                    ax.add_collection(PatchCollection(patch, linewidth=0, edgecolor='black', facecolor=self.param.loc[s, 'color']))
                    #ax.scatter(sub['x'], sub['y'], s = 0.01, color=self.param.loc[s, 'color'])
                    
        if self.boundaries == True:
            self.Load(f'{files.input}/{cat}_Boundaries.csv')
            ax = self.PlotPatch(ax, cat, self.df, res, linewidth = 0, edgecolor = 'black', facecolor = 'black', cmap = None, norm = 'norm')
            boundaries = 'Boundaries'
        else:
            boundaries = 'Noboundaries'
            
        self.barScale(cat, ax, self.df, self.barLegend, text = self.text)
        plt.axis('off')
        plt.axis('scaled')
        self.Save(fig, f'{files.output}/{cat}_Sort{self.sort}{boundaries}Map.png')
                
               
    def ColorBar(self, files, cat):
    
        ebsd = self.Load(f'{files.input}/{cat}_all_EBSD.csv')
        if self.field not in self.df.columns:
            grains = self.Load(f'{files.input}/{cat}_all_Grains.csv')
            ebsd = ebsd.merge(grains, left_on='grain', right_on='id' , how='outer')
        
        if self.minimum == None:
            self.minimum = np.min(ebsd[self.field])
        if self.maximum == None:
            self.maximum = np.max(ebsd[self.field])
                
        if self.color == 'sscat':
            for ssc in files.sscat:
                fig, ax = self.ParamPlot()
                fraction = 1  # .05
                self.ColorScale(self.param.loc[ssc, 'color'], min = self.minimum, max = self.maximum, step = int(self.maximum - self.minimum))
                norm = mpl.colors.Normalize(vmin=self.minimum, vmax=self.maximum)
                cbar = ax.figure.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=self.colorScale), ax=ax, pad=.05, extend='both', fraction=fraction)
                ax.axis('off')
                self.Save(fig, f"{files.output}/{self.field}_{self.param.loc[ssc, 'color']}_{self.minimum}-{self.maximum}.png")
        else:
            fig, ax = self.ParamPlot()
            fraction = 1  # .05
            self.ColorScale(self.color, min = self.minimum, max = self.maximum, step = int(self.maximum - self.minimum))
            norm = mpl.colors.Normalize(vmin=self.minimum, vmax=self.maximum)
            cbar = ax.figure.colorbar(mpl.cm.ScalarMappable(norm=norm, cmap=self.colorScale), ax=ax, pad=.05, extend='both', fraction=fraction)
            ax.axis('off')
            self.Save(fig, f'{files.output}/{cat}_{self.field}_{self.color}_{self.minimum}-{self.maximum}.png')
                
        

    def Pie(self, files, file = None):
        if file == None:
            self.Load(f'{files.stats}/resume.csv')
            self.df.index = self.df.id
        else:
            self.Load(file)

        #self.df = self.df[self.df['sort'] == f'{self.column}{self.value}']
        self.df = self.df[self.df['subcat'] == 'all']
        self.df = self.df[self.df['sscat'] != 'all']
        
        for c in files.cat:
            cat = self.df[self.df['cat'] == c]
            
            labels = []
            values = []
            colours = []

            for ssc in sorted(set(cat.sscat)):
                labels.append(ssc)
                values.append(cat.loc[f'{c}_{ssc}_all', f'%catArea'])
                colours.append(self.param.loc[ssc, 'color'])
   
            fig, ax = self.ParamPlot()
            ax.pie(values, labels = labels, colors = colours, normalize = True, autopct='%1.1f%%')
            self.Save(fig, f'{files.output}/{c}_pie.png')


    def PieSubcat(self, files, file = None):
        if file == None:
            self.Load(f'{files.stats}/resume.csv')
            self.df.index = self.df.id
        else:
            self.Load(file)

        self.df = self.df[self.df['sort'] == f'{self.sort}']
        self.df = self.df[(self.df['sscat'] != 'all') & (self.df['subcat'] != 'all')]
        
        for c in files.cat:
            cat = self.df[self.df['cat'] == c]
            
            labels = []
            values = []
            colours = []
            hatches = []

            for ssc in sorted(set(cat.sscat)):
                for s in sorted(set(cat.subcat)):
                    labels.append(f'{ssc}_{s}')
                    values.append(cat.loc[f'{c}_{ssc}_{s}_{self.sort}', f'%catArea'])
                    colours.append(self.param.loc[ssc, 'color'])
                    hatches.append(self.param.loc[s, 'hatches'])

            fig, ax = self.ParamPlot()
            values = np.nan_to_num(values)
            ax.pie(values, colors = colours, hatch = hatches, wedgeprops = {"edgecolor" : "black", 'linewidth': 1.5, 'antialiased': True})
            self.Save(fig, f'{files.output}/{c}_pieSubcat{self.sort}.png')



    def Histogram(self, files, cat, sscat):
        self.Load(f'{files.input}/{cat}_{sscat}_Grains.csv', sort = True)
        
        area = pd.read_csv(f'{files.stats}/resume.csv', sep = ';')
        area.index = area.id
        try:
            nneo = round(area.loc[f'{cat}_{sscat}_neo_{self.sort}', '%sscatArea']*100, 2)
        except:
            nneo = 0
        try:
            nneo2 = round(area.loc[f'{cat}_{sscat}_neo_{self.sort}', '%catArea']*100, 2)
        except:
            nneo2 = 0
        m = round(area.loc[f'{cat}_{sscat}_all', '%catArea']*100, 2)
        
        # values
        fig, ax = self.ParamPlot()
        plt.rcParams["font.family"] = self.fontFamily
        plt.rcParams["font.size"] = self.fontSize
        ax.hist(self.df[self.field], density = True, facecolor = self.param.loc[sscat, 'color'], edgecolor = 'black', bins = 'auto', weights = None)
        ax.set_xlabel(self.legend)
        ax.set_ylabel('Frequency')
        ax.set_title(f'{len(self.df[self.field])} grains, {m}% of sample area ({self.sort})')
        self.Save(fig, f'{files.output}/{cat}_{sscat}_all_hist{self.field}_weightNone.png')

        # weighted values
        fig, ax = self.ParamPlot()
        plt.rcParams["font.family"] = self.fontFamily
        plt.rcParams["font.size"] = self.fontSize
        hist, bins = np.histogram(self.df[self.field], weights = self.df[self.weight], bins = self.bins)
        ax.hist(self.df[self.field], bins = self.bins, weights = self.df[self.weight], facecolor = self.param.loc[sscat, 'color'], edgecolor = 'black')
        ax.set_xlabel(self.legend)
        ax.set_ylabel('total %')
        ax.set_title(f'{len(self.df[self.field])} grains, {m}% of sample area ({self.sort})')

        ax.set_ylim([np.min(hist), np.max(hist)])
        self.weights = self.df[self.weight]
        self.ticks(ax)
        self.Save(fig, f'{files.output}/{cat}_{sscat}_all_hist{self.field}_weight{self.weight}.png')

        # weighted values
        fig, axes = plt.subplots(1, 2, gridspec_kw = {'width_ratios': [2, 2]}, figsize=(self.width, self.height), dpi = self.dpi)
        plt.rcParams["font.family"] = self.fontFamily
        plt.rcParams["font.size"] = self.fontSize

        neo = self.df[self.df[self.sort] == 'neo']
        porph = self.df[self.df[self.sort] == 'porph']

        #axes[0].hist(neo[self.field], density = False, bins = self.bins, color = 'gray', alpha = 0.4, weights = neo[self.weight])

        hist, bins = np.histogram(neo[self.field], weights = neo[self.weight], bins = self.bins)
        axes[0].plot(list(bins)[0:self.bins], hist, color = self.param.loc['neo', 'color'])
        axes[0].tick_params(axis = 'y', labelcolor = self.param.loc['neo', 'color'])
        axes[0].set_ylim([np.min(hist), np.max(hist)])
        self.weights = neo[self.weight]
        axes[0].yaxis.label.set_color(self.param.loc['neo', 'color'])
        self.ticks(axes[0])

        ax2 = axes[0].twinx()
        #ax2.hist(porph[self.field], density = False, bins = self.bins, color = 'black', alpha = 0.4, weights = porph[self.weight])
        hist, bins = np.histogram(porph[self.field], weights = porph[self.weight], bins = self.bins)
        ax2.plot(list(bins)[0:self.bins], hist, color = self.param.loc['porph', 'color'])
        ax2.tick_params(axis = 'y', labelcolor = self.param.loc['porph', 'color'])
        ax2.yaxis.label.set_color(self.param.loc['porph', 'color'])
        ax2.set_ylim([np.min(hist), np.max(hist)])
        self.weights = porph[self.weight]
        self.ticks(ax2)

        ax3 = axes[1].twinx()
        axes[1].set_yticklabels([])
        hist, bins = np.histogram(self.df[self.field], weights = self.df[self.weight], bins = self.bins)
        #ax3.plot(list(bins)[0:self.bins], hist, color = self.param.loc[sscat, 'colour'])
        ax3.hist(self.df[self.field], bins = self.bins, weights = self.df[self.weight], facecolor = self.param.loc[sscat, 'color'], edgecolor = 'black')
        ax3.tick_params(axis = 'y', labelcolor = self.param.loc[sscat, 'color'])
        ax3.yaxis.label.set_color(self.param.loc[sscat, 'color'])
        ax3.set_ylim([np.min(hist), np.max(hist)])
        self.weights = self.df[self.weight]
        self.ticks(ax3)

        ax.set_title(f'{len(self.df[self.field])} values')
        axes[0].set_xlabel(self.legend)
        axes[0].set_ylabel('neoblates %')
        ax2.set_ylabel('porphyroclastes %')
        ax3.set_xlabel(self.legend)
        axes[0].set_xlabel(self.legend)
        ax3.set_ylabel('total %')
        fig.suptitle(f'{nneo}% neoblasts in mineral fraction, {nneo2}% in thin section fraction')
        fig.tight_layout()
        self.Save(fig, f'{files.output}/{cat}_{sscat}_subcat_hist{self.field}weight{self.weight}{self.sort}.png')



    def heatmap(data, row_labels, col_labels, cbar_kw=None, cbarlabel="", **kwargs):
        """
        Create a heatmap from a numpy array and two lists of labels.

        Parameters
        ----------
        data
            A 2D numpy array of shape (M, N).
        row_labels
            A list or array of length M with the labels for the rows.
        col_labels
            A list or array of length N with the labels for the columns.
        ax
            A `matplotlib.axes.Axes` instance to which the heatmap is plotted.  If
            not provided, use current axes or create a new one.  Optional.
        cbar_kw
            A dictionary with arguments to `matplotlib.Figure.colorbar`.  Optional.
        cbarlabel
            The label for the colorbar.  Optional.
        **kwargs
            All other arguments are forwarded to `imshow`.
        """

        if ax is None:
            ax = plt.gca()

        if cbar_kw is None:
            cbar_kw = {}

        # Plot the heatmap
        im = ax.imshow(data, **kwargs)

        # Create colorbar
        cbar = ax.figure.colorbar(im, ax=ax, **cbar_kw)
        cbar.ax.set_ylabel(cbarlabel, rotation=-90, va="bottom")

        # Show all ticks and label them with the respective list entries.
        ax.set_xticks(np.arange(data.shape[1]), labels=col_labels)
        ax.set_yticks(np.arange(data.shape[0]), labels=row_labels)

        # Let the horizontal axes labeling appear on top.
        ax.tick_params(top=True, bottom=False, labeltop=True, labelbottom=False)

        # Rotate the tick labels and set their alignment.
        plt.setp(ax.get_xticklabels(), rotation=-30, ha="right", rotation_mode="anchor")

        # Turn spines off and create white grid.
        ax.spines[:].set_visible(False)

        ax.set_xticks(np.arange(data.shape[1]+1)-.5, minor=True)
        ax.set_yticks(np.arange(data.shape[0]+1)-.5, minor=True)
        ax.grid(which="minor", color="w", linestyle='-', linewidth=3)
        ax.tick_params(which="minor", bottom=False, left=False)

        return im, cbar


    def annotate_heatmap(im, data=None, valfmt="{x:.2f}", textcolors=("black", "white"), threshold=None, **textkw):
        """
        A function to annotate a heatmap.

        Parameters
        ----------
        im
            The AxesImage to be labeled.
        data
            Data used to annotate.  If None, the image's data is used.  Optional.
        valfmt
            The format of the annotations inside the heatmap.  This should either
            use the string format method, e.g. "$ {x:.2f}", or be a
            `matplotlib.ticker.Formatter`.  Optional.
        textcolors
            A pair of colors.  The first is used for values below a threshold,
            the second for those above.  Optional.
        threshold
            Value in data units according to which the colors from textcolors are
            applied.  If None (the default) uses the middle of the colormap as
            separation.  Optional.
        **kwargs
            All other arguments are forwarded to each call to `text` used to create
            the text labels.
        """

        if not isinstance(data, (list, np.ndarray)):
            data = im.get_array()

        # Normalize the threshold to the images color range.
        if threshold is not None:
            threshold = im.norm(threshold)
        else:
            threshold = im.norm(data.max())/2.

        # Set default alignment to center, but allow it to be overwritten by textkw.
        kw = dict(horizontalalignment="center", verticalalignment="center")
        kw.update(textkw)

        # Get the formatter in case a string is supplied
        if isinstance(valfmt, str):
            valfmt = matplotlib.ticker.StrMethodFormatter(valfmt)

        # Loop over the data and create a `Text` for each "pixel".
        # Change the text's color depending on the data.
        texts = []
        for i in range(data.shape[0]):
            for j in range(data.shape[1]):
                kw.update(color=textcolors[int(im.norm(data[i, j]) > threshold)])
                text = im.axes.text(j, i, valfmt(data[i, j], None), **kw)
                texts.append(text)

        return texts


    def PlotPercentBoundary(self, files, cat):

        
        df = pd.read_csv(f'{files.input}/{self.table}.csv', sep = ';')

        if 'all' in files.sscat:
            liste = list(files.sscat.copy())
            liste.remove('all')
            liste.sort()

        li = [self.labels[l] for l in liste]

        size = len(liste)
        size = int(size)
      
        for idd in list(product(self.sort, self.subcat)):

            sort = idd[0]
            sub = idd[1]
            listId = list(df['id'])
            df.index = df['id']
            matrix = np.zeros((size, size))
        
            for it in list(product(liste, liste)):
                
                grains = liste.index(it[0])
                neighbors = liste.index(it[1])
                grains = int(grains)
                neighbors = int(neighbors)

                try:
                    val = df.loc[f'{cat}_{it[0]}_{sub}_{sort}', f'{self.on}%boundary{it[1]}']
                    val = round(val[1]*100, 2)
                except:
                    val = 0

                if val > 0:
                    val = val
                else:
                    val = 0

                matrix[grains, neighbors] = val

            self.fontSize = 12
            self.dpi = 900
            fig, ax = self.ParamPlot()

            fig, ax = plt.subplots()
            im = ax.imshow(matrix, cmap = self.cmap)

            # Show all ticks and label them with the respective list entries
            ax.set_xticks(np.arange(len(liste)), labels=li)
            ax.set_yticks(np.arange(len(liste)), labels=li)

            # Rotate the tick labels and set their alignment.
            plt.setp(ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor")

            # Loop over data dimensions and create text annotations.
            for i in range(len(liste)):
                for j in range(len(liste)):
                    text = ax.text(j, i, matrix[i, j], ha="center", va="center", color="w")

            ax.set_title("% of length shared between minerals")
            plt.savefig(f'{files.output}/{cat}_{sub}_{sort}_{self.on}.png')


