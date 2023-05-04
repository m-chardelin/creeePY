from path import *
from creeePY import Files, Statistics, Display, Tex
import os

# Directories

files = Files.Files(analysis, 'ZAB')

files.SetFolders(display = 'display', calculations = 'calculations', graphs = 'graphs', plot = 'plot', param = 'param', stats = 'stats', tex = 'tex', config = 'config', ctf = 'ctf', results = 'results', verif = 'verif', auto = True)

files.SetSubFolders(files.tex, ['figures', 'text'])

files.CopyFiles(files.calculations, [files.display], extension = 'csv')

# Display

files.SetFiles(inp = files.display, out = files.plot)
files.SetCats(files.display, '.csv')
disp = Display.Display(files)

columns = ['EGD', 'EGD', 'GOS', 'GOS', 'GOS', 'GOS', 'EGD']
values = ['manuel', 'mixte', 2, 1, 1.5, 0.5, 200]

for eps in [False, True]:
    files.SetFiles(inp = files.display, out = files.plot)
    disp.SetParam(fontFamily = 'serif', fontSize = 18, height = 30, width = 15, dpi = 400, version = 'EN', eps = eps, sort = 'EGD_200', barLegend = '12 mm', grad = 6, text = None)
        
    #disp.Iteration(files, disp.PhasesMap)
    #disp.Iteration(files, disp.BoundariesMap)

    disp.SetParam(minimum = 0, maximum = 15, color = 'sscat', field = 'grod', colorbar = False, boundaries = True)
    #disp.Iteration(files, disp.FieldMap)
    #disp.Iteration(files, disp.ColorBar)

    disp.SetParam(minimum = 'all', maximum = 'all', color = 'black', field = 'area', colorbar = False, boundaries = True, all = True)
    disp.Iteration(files, disp.FieldMap)
    #disp.Iteration(files, disp.ColorBar)

    disp.SetParam(minimum = 'all', maximum = 'all', color = 'teal', field = 'GOS', colorbar = False, boundaries = True, all = True)
    #disp.Iteration(files, disp.FieldMap)
    #disp.Iteration(files, disp.ColorBar)

    disp.SetParam(minimum = 0, maximum = 4, color = 'sscat', field = 'kam', colorbar = False, boundaries = True)
    disp.Iteration(files, disp.FieldMap)
    #disp.Iteration(files, disp.ColorBar)

    for s in ['EGDmixte']:
        disp.SetParam(subcat = ['rex', 'porph'], sort = s, boundaries = True)
        #disp.Iteration(files, disp.SortMap)
        disp.SetParam(sort = s, boundaries = False)
        #disp.Iteration(files, disp.SortMap)


    for col, val in zip(columns, values):

        disp.SetParam(column = col, value = val)
        #disp.Pie(files)
        #disp.PieSubcat(files)

        disp.SetParam(height = 8, width = 10, bins = 40, density = False, task = 'Grains', weight = 'area', fontSize = 12)
        disp.SetParam(field = 'EGD', legend = 'EGD (µm)')
        #disp.Iteration(files, disp.Histogram, iterMineral = True)
        #disp.SetParam(field = 'shapeFactor', legend = 'Shape Factor')
        #disp.Iteration(files, disp.Histogram, iterMineral = True)
        #disp.SetParam(field = 'GOS', legend = 'GOS')
        #disp.Iteration(files, disp.Histogram, iterMineral = True)


files.CopyFiles(files.plot, [files.figures], extension = 'eps')

taskCat = ['PhasesMap', 'BoundariesMap', 'kamMap', 'grodMap', 'histEGD', 'histshapeFactor', 'histGOS', 'SortEGD']
files.SortFiles([files.plot], taskCat)
